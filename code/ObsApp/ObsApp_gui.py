# -*- coding: utf-8 -*-

"""
Created on Oct 21, 2022

Modified on Nov 20, 2023

refered from SCP of original IGRINS
@author: hilee
"""

import sys, os
from ui_ObsApp import *
from ObsApp_def import *

import threading

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from Libs.MsgMiddleware import *
from Libs.logger import *
import Libs.SetConfig as sc

import time as ti
from shutil import copyfile
from distutils.util import strtobool

import subprocess
import numpy as np
#from scipy.ndimage.interpolation import rotate
from scipy.optimize import curve_fit
import astropy.io.fits as fits 

import Libs.zscale as zs
import TMCF_Functions_jj as tmcfmask

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle, Circle

              
class MainWindow(Ui_Dialog, QMainWindow):
    
    def __init__(self, simul):  #simulation mode: True
        super().__init__()
                        
        self.init_widget_rect = []
        self.prev_widget_rect = []      
        
        self.iam = "ObsApp"
        self.simulation = strtobool(simul)
        
        self.setupUi(self)
        
        self.log = LOG(WORKING_DIR+self.iam)  
        self.show_log_list(INFO, "start")
        
        self.setWindowTitle("ObsApp 2.0")     
        
        # canvas        
        self.image_ax = [None for _ in range(3)]
        self.image_canvas = [None for _ in range(3)]
        for i in range(3):
            _image_fig = Figure(figsize=(4, 4), dpi=100)
            self.image_ax[i] = _image_fig.add_subplot(111)            
            if i == 1:
                _image_fig.subplots_adjust(left=0.02,right=1.03,bottom=0.02,top=1.03) 
            elif i == 2:
                _image_fig.subplots_adjust(left=0.035,right=0.96,bottom=0.043,top=0.96) 
            else:
                _image_fig.subplots_adjust(left=0.01,right=0.99,bottom=0.01, top=0.99) 
            self.image_canvas[i] = FigureCanvas(_image_fig)
        
        vbox_svc = [None for _ in range(4)]               
        vbox_svc[0] = QVBoxLayout(self.frame_svc)
        vbox_svc[0].addWidget(self.image_canvas[IMG_SVC])
        vbox_svc[1] = QVBoxLayout(self.frame_expand)
        vbox_svc[1].addWidget(self.image_canvas[IMG_EXPAND])
        vbox_svc[2] = QVBoxLayout(self.frame_fitting)
        vbox_svc[2].addWidget(self.image_canvas[IMG_FITTING])
        #vbox_svc[3] = QVBoxLayout(self.frame_profile)
        #vbox_svc[3].addWidget(self.image_canvas[IMG_PROFILE])
        
        self.clean_ax(self.image_ax[IMG_SVC])
        self.clean_ax(self.image_ax[IMG_EXPAND])
        self.clean_ax(self.image_ax[IMG_FITTING], False)
        #self.clean_ax(self.image_ax[IMG_PROFILE])
        
        self.image_ax[IMG_FITTING].tick_params(axis='x', labelsize=6, pad=-12)
        self.image_ax[IMG_FITTING].tick_params(axis='y', labelsize=6, pad=-14)
                
        #---------------------------------------------------------
        # load ini file
        cfg = sc.LoadConfig(WORKING_DIR + "ObsApp/ObsApp.ini")
              
        self.ics_ip_addr = cfg.get(MAIN, "ip_addr")
        self.ics_id = cfg.get(MAIN, "id")
        self.ics_pwd = cfg.get(MAIN, "pwd")
        
        self.InstSeq_ex = cfg.get(MAIN, 'InstSeq_exchange')
        self.InstSeq_q = cfg.get(MAIN, 'InstSeq_routing_key')
        
        self.ObsApp_ex = cfg.get(MAIN,  'ObsApp_exchange')     #ObsApp -> InstSeq, DCSS
        self.ObsApp_q = cfg.get(MAIN, 'ObsApp_routing_key')
                
        #self.temp_limit = float(cfg.get(HK, 'temp-limit'))    #for abs(normal) range
        self.Period = int(cfg.get(HK,'hk-monitor-intv'))
        
        slit_img_flip = bool(int(cfg.get(SC, 'slit-image-flip')))
        if slit_img_flip:
            self.slit_image_flip_func = lambda im: np.rot90(im, 2) #np.fliplr(np.rot90(im))
            self.slit_coord_abs_flip_func = lambda x,y: (2048-y, 2048-x)
        else:
            self.slit_image_flip_func = lambda im: im #np.rot90(im)
            self.slit_coord_abs_flip_func = lambda x,y: (x, y)
                    
        global SLIT_CEN, SLIT_WID, SLIT_LEN, SLIT_ANG, ZOOMW, CONTOURW, PIXELSCALE
        try:
            tmp = cfg.get(SC, 'slit-cen').split(",")
            SLIT_CEN = self.slit_coord_abs_flip_func(float(tmp[0]), float(tmp[1]))
        except:
            SLIT_CEN = (0,0)
            msg = 'Slit Center Parameter Error: %s' % (self.cfg.get(SC, 'slit-cen'),)
            self.show_log_list(ERROR, msg)
                    
        SLIT_WID = float(cfg.get(SC,'slit-wid'))
        SLIT_LEN = float(cfg.get(SC,'slit-len'))
        SLIT_ANG = float(cfg.get(SC,'slit-ang'))
        
        A_pos = cfg.get(SC, 'A_pos').split(",")
        B_pos = cfg.get(SC, 'B_pos').split(",")
        self.A_x, self.A_y = float(A_pos[0]), float(A_pos[1])
        self.B_x, self.B_y = float(B_pos[0]), float(B_pos[1])

        slit_cen_pq = cfg.get(SC, 'center_pq').split(",")
        self.slit_cen_p, self.slit_cen_q = float(slit_cen_pq[0]), float(slit_cen_pq[1])
        
        A_pos_pq = cfg.get(SC, 'A_pos_pq').split(",")
        B_pos_pq = cfg.get(SC, 'B_pos_pq').split(",")
        self.A_p, self.A_q = float(A_pos_pq[0]), float(A_pos_pq[1])
        self.B_p, self.B_q = float(B_pos_pq[0]), float(B_pos_pq[1])
        
        
        ZOOMW = int(cfg.get(SC, 'zoomw'))
        CONTOURW = int(cfg.get(SC, 'contourw'))
        PIXELSCALE = float(cfg.get(SC, 'pixelscale'))
        self.fwhm_mode = int(cfg.get(SC, 'fwhm-mode'))
        self.fwhm_mode_value = float(cfg.get(SC, 'fwhm-mode-value'))
        
        self.out_of_number_svc = int(cfg.get(SC, 'out-of-number-svc'))
        
        self.svc_path = cfg.get(DCS,'data-location')
        
        self.setup_sw_offset_window(self.frame_profile)
        
        self.key_to_label = dict()
        self.dtvalue, self.heatlabel = dict(), dict()
        self.temp_lower_warning, self.temp_lower_normal = dict(), dict()
        self.temp_upper_normal, self.temp_upper_warning = dict(), dict()
        self.det_sts = dict()
        
        self.label_list = ["tmc2-a", "tmc2-b", "tmc3-b"]
        self.dpvalue = DEFAULT_VALUE
        
        self.ig2_health = GOOD
        
        for k in self.label_list:
            hk_list = cfg.get(HK, k).split(",")
            self.key_to_label[k] = hk_list[0]
            self.temp_lower_warning[k] = hk_list[1]
            self.temp_lower_normal[k] = hk_list[2]
            #self.temp_normal[k] = hk_list[3]
            self.temp_upper_normal[k] = hk_list[4]
            self.temp_upper_warning[k] = hk_list[5]
            
            self.dtvalue[k] = DEFAULT_VALUE
            self.heatlabel[k] = DEFAULT_VALUE     
            
            self.det_sts[k] = "good"                   
                            
        self.producer = None    # for Inst. Sequencer, DCSS
        self.consumer_InstSeq = None
        self.consumer_dcs = [None for _ in range(DC_CNT)]
        self.consumer_sub = [None for _ in range(SUB_CNT)]
        
        #self.Qth_dcs = [None for _ in range(DC_CNT)]
        
        #self.consumer_virtual_tcs = None
        
        self.param_InstSeq = None
        self.param_dcs = [None for _ in range(DC_CNT)]
        
        _svc_x, _svc_y = float(SLIT_CEN[0]), float(SLIT_CEN[1])
        self.guide_x, self.guide_y = _svc_x, _svc_y
        self.svc_cut_x, self.svc_cut_y = 400, 400
        self.click_x, self.click_y = _svc_x, _svc_y
        self.off_x, self.off_y = self.click_x, self.click_y
        self.click_p, self.click_q = 0, 0
        
        self.height, self.sigma, self.background = 0.0, 0.0, 0.0
        self.cen_x, self.cen_y = 0, 0   # center in full coordination after fitting
                
        self.fitting_clicked = False  #False: fitting, True: contour
        
        self.cur_frame = None #A, B or nothing
        self.prev_frame = self.cur_frame
        
        self.find_center = False
                
        #--------------------------------
        # 0 - SVC, 1 - H_K
        
        self.dcss_ready = False
        self.acquiring = [False for _ in range(DC_CNT)]
        self.dcss_setparam = False
        
        self.cur_save_cnt = 0
        self.cur_guide_cnt = 0
        self.center_ra, self.center_dec = [], []
        
        self.NFS_load_time = 0
                
        self.svc_mode = SINGLE_MODE
        self.cal_waittime = [0, 0]
        self.stop_clicked = False   # for continuous mode
        
        self.svc_header = None
        self.svc_img = None
        self.svc_img_cut = None
        
        self.sky_data = None
        self.sky_exp_time = 0.
        
        self.fitsfullpath = None
        self.file_name = None
           
        self._init_mask()
        
        self.resize_enable = True
        
        self.mmin, self.mmax = 0, 1000

        # progress bar     
        self.prog_timer = [None, None]
        self.cur_prog_step = [None, None]
       
        #20231005
        self.progressBar_svc.setValue(0)
        self.progressBar_obs.setValue(0)

        # elapsed
        self.elapsed_obs_timer = None
        self.elapsed_obs = 0.0
        self.measure_T = 0
        
        # from InstSeq, Position angle
        self.PA = 0
        
        self.draw = False
        #--------------------------------
        
        self.init_events() 
        
        # Instrument Status
        self.label_is_health.setText("---")
        self.label_GDSN_connection.setText("---")
        self.label_GMP_connection.setText("---")
        self.label_state.setText("Idle")
        self.label_action_state.setText("---")        
        
        self.label_vacuum.setText("---")
        self.label_temp_detH.setText("---")
        self.label_temp_detK.setText("---")
        self.label_temp_detS.setText("---")
        self.label_heater_detH.setText("---")
        self.label_heater_detK.setText("---")
        self.label_heater_detS.setText("---")   
        
        # Science Observation
        self.label_data_label.setText("---")
        self.label_obs_state.setText("Idle")
        self.label_sampling_number.setText("---")
        self.label_exp_time.setText("---")
        self.label_time_left.setText("---")
        self.label_IPA.setText("---") 
        
        # Slit View Camera
        self.label_svc_filename.setText("---")
        self.label_svc_state.setText("---")
        self.e_svc_fowler_number.setText("1")
        self.e_svc_exp_time.setText("1.63")
        
        self.bt_single.setText("Exposure")
        
        # temp
        fname = ti.strftime("SDCS_%02Y%02m%02d_", ti.localtime())
        self.e_repeat_file_name.setText(fname)
        self.e_saving_number.setText(str(self.out_of_number_svc))
        
        self.e_offset.setText("1")
        
        self.label_cur_Idx.setText("0 /")
        self.e_averaging_number.setText("5")
        
        self.radio_raw.setChecked(True)
        self.radio_zscale.setChecked(True)
        
        self.label_zscale.setText("---")
        self.e_mscale_min.setText("1000")
        self.e_mscale_max.setText("5000")   
        
        self.radio_none.setChecked(True)
        
        #self.editlist_loglist.clear()
                
        # connect to rabbitmq
        self.connect_to_server_ObsApp_ex()
        
        self.connect_to_server_InstSeq_q()  #InstSeq
        self.connect_to_server_sub_q()  #TC2, TC3, VM, uploader
        self.connect_to_server_dcs_q()  #DCSS, DCSH, DCSK
        
        #self.connect_to_server_virtual_tcs_q()
                       
        self.InstSeq_timer = QTimer(self)
        self.InstSeq_timer.setInterval(1)
        self.InstSeq_timer.timeout.connect(self.InstSeq_data_processing)
        self.InstSeq_timer.start()
        
        '''
        self.svc_cmd_timer = QTimer(self)
        self.svc_cmd_timer.setInterval(1)
        self.svc_cmd_timer.timeout.connect(self.svc_progressbar_monit)
        self.svc_cmd_timer.start()
        self.svc_progressbar_start = False
        
        self.prog_timer[SVC] = QTimer(self)
        self.prog_timer[SVC].timeout.connect(lambda: self.show_progressbar(SVC)) 
        
        self.hk_cmd_timer = QTimer(self)
        self.hk_cmd_timer.setInterval(1)
        self.hk_cmd_timer.timeout.connect(self.hk_progressbar_monit)
        self.hk_cmd_timer.start()
        self.hk_progressbar_start = False
        
        self.prog_timer[H_K] = QTimer(self)
        self.prog_timer[H_K].timeout.connect(lambda: self.show_progressbar(H_K))
        '''
        self.show_sub_timer = QTimer(self)
        self.show_sub_timer.setInterval(self.Period/2 * 1000)
        self.show_sub_timer.timeout.connect(self.sub_data_processing)
        self.show_sub_timer.start()
        
        self.show_dcs_timer = [None for _ in range(DC_CNT)]
        for idx in range(DC_CNT):
            self.show_dcs_timer[idx] = QTimer(self)
            self.show_dcs_timer[idx].setInterval(1)
            if idx == SVC:
                self.show_dcs_timer[idx].timeout.connect(self.dcs_data_processing_SVC) 
            else:
                self.show_dcs_timer[idx].timeout.connect(lambda: self.dcs_data_processing_HK(idx))
            self.show_dcs_timer[idx].start()    
                        
        msg = "%s DCSS %d" % (CMD_INIT2_DONE, self.simulation)
        self.publish_to_queue(msg)
                           
        self.auto_save_image()         
        self.set_off_slit()
        
        self.select_log_none()
        
        self.sw_slit_star_init()

        
        
    def closeEvent(self, event: QCloseEvent) -> None:        
        
        self.InstSeq_timer.stop()
        #self.svc_cmd_timer.stop()
        self.show_sub_timer.stop()
        #self.hk_cmd_timer.stop()
        for idx in range(DC_CNT):
            self.show_dcs_timer[idx].stop()
        
        self.show_log_list(DEBUG, "Closing %s : " % sys.argv[0])
        self.show_log_list(DEBUG, "This may take several seconds waiting for threads to close")
                            
        if self.producer != None:
            self.producer.__del__()
        
        '''    
        self.producer.channel.close()
        self.consumer_InstSeq.channel.close()
        for i in range(DC_CNT):
            self.consumer_dcs[i].channel.close()
            self.consumer_sub[i].channel.close()
        '''
                            
        self.show_log_list(DEBUG, "Closed!")
        
        return super().closeEvent(event)
    
    
    def init_events(self):
        
        #self.editlist_loglist.setMaximumBlockCount(40)
        self.init_widget_rect = [None for _ in range(20)]
                
        self.image_canvas[IMG_SVC].mpl_connect('button_press_event', self.image_leftclick)
        self.image_canvas[IMG_FITTING].mpl_connect('button_press_event', self.fitting_leftclick)
        
        self.chk_continue.clicked.connect(self.set_continue_mode)
        self.bt_single.clicked.connect(self.single)
        
        self.chk_auto_save.clicked.connect(self.auto_save_image)
        self.e_saving_number.editingFinished.connect(self.change_outoufnumber_svc)
        self.bt_repeat_filesave.clicked.connect(self.manual_filesave)
        
        self.bt_center.clicked.connect(self.set_center)
        self.chk_off_slit.clicked.connect(self.set_off_slit)
        self.bt_set_guide_star.clicked.connect(self.set_guide_star)
        
        self.bt_plus_p.clicked.connect(lambda: self.move_p(False))
        self.bt_minus_p.clicked.connect(lambda: self.move_p(True))
        self.bt_plus_q.clicked.connect(lambda: self.move_q(True))
        self.bt_minus_q.clicked.connect(lambda: self.move_q(False))
        
        self.bt_slow_guide.clicked.connect(self.slow_guide)
        
        self.chk_view_drawing.clicked.connect(self.view_drawing)
        self.chk_view_drawing.setChecked(True)
        
        self.radio_raw.clicked.connect(self.select_raw)
        self.radio_sub.clicked.connect(self.select_sub)
        self.bt_mark_sky.clicked.connect(self.mark_sky)
       
        self.radio_zscale.clicked.connect(self.select_zscale)
        self.radio_mscale.clicked.connect(self.select_mscale)

        self.radio_none.clicked.connect(self.select_log_none)
        self.radio_show_logfile.clicked.connect(self.select_log_file)
        self.radio_show_loglist.clicked.connect(self.select_log_list)
        
        self.bt_single.setEnabled(False)
        self.bt_slow_guide.setEnabled(False)
        self.bt_set_guide_star.setEnabled(False)
        
        
    def _init_mask(self):
        # make the mask from mask.template
        hdul = fits.open(WORKING_DIR + "ObsApp_pack/code/ObsApp/slitmaskv0_igrins2.fits")
        mask = hdul[0].data     
        self.mask = self.slit_image_flip_func(mask)
        hdul.close()
         
    #--------------------------------------------------------
    # ObsApp publisher
    def connect_to_server_ObsApp_ex(self):
        self.producer = MsgMiddleware(self.iam, self.ics_ip_addr, self.ics_id, self.ics_pwd, self.ObsApp_ex)      
        self.producer.connect_to_server()
        self.producer.define_producer()
    
    
    def publish_to_queue(self, msg):
        if self.producer == None:
            return
        
        self.producer.send_message(self.ObsApp_q, msg)
        msg = "%s ->" % msg
        self.show_log_list(INFO, msg)
    
    
    #--------------------------------------------------------
    # InstSeq queue
    def connect_to_server_InstSeq_q(self):
        self.consumer_InstSeq = MsgMiddleware(self.iam, self.ics_ip_addr, self.ics_id, self.ics_pwd, self.InstSeq_ex)      
        self.consumer_InstSeq.connect_to_server()
        self.consumer_InstSeq.define_consumer(self.InstSeq_q, self.callback_InstSeq)       
                
        th = threading.Thread(target=self.consumer_InstSeq.start_consumer)
        th.daemon = True
        th.start()
    
    
    def callback_InstSeq(self, ch, method, properties, body):
        cmd = body.decode()
        msg = "<- [InstSeq] %s" % cmd
        self.show_log_list(INFO, msg)
        self.param_InstSeq = cmd
    
                
        
    #--------------------------------------------------------
    # Vitual TCS queue
    '''
    def connect_to_server_virtual_tcs_q(self):
        self.consumer_virtual_tcs = MsgMiddleware(self.iam, self.ics_ip_addr, self.ics_id, self.ics_pwd, "MovePosition.ex")      
        self.consumer_virtual_tcs.connect_to_server()
        self.consumer_virtual_tcs.define_consumer("MovePosition.q", self.callback_virtual_tcs)       
        
        print("thread; virtual_tcs")
        self.Qth_virtual_tcs = monitoring(self.consumer_virtual_tcs)
        self.Qth_virtual_tcs.start()
        
        #th = threading.Thread(target=self.consumer_virtual_tcs.start_consumer)
        #th.daemon = True
        #th.start()
    
    
    def callback_virtual_tcs(self, ch, method, properties, body):
        cmd = body.decode()
        msg = "<- [MovePosition] %s" % cmd
        self.show_log_list(INFO, msg)
        print(cmd)
        param = cmd.split()
        
        #_x, _y = self.calc_xy_to_pq(float(param[1]), float(param[2]), True)
        
        #change 20231006
        #current p and q value!!!
        if param[0] == MOVEPOS_P_Q:
            #th = [0.2, 0.2]
            #ON-OFF
            #A-B
            #temp!!!

            #if self.A_p == float(param[1]) and self.A_q == float(param[2]):
            #    self.cur_frame = A_BOX
            #elif self.A_p == float(param[1]) and self.A_q == float(param[2]) * 2:
            #    self.cur_frame = A_BOX
            #elif self.B_p == float(param[1]) and self.B_q == float(param[2]) * 2:
            #    self.cur_frame = B_BOX            
            
            self.cur_frame = A_BOX
            if float(param[2]) > 0:
                self.cur_frame = B_BOX
                
            #print(_x, _y)
            #_x, _y = SLIT_CEN[0]+_x, SLIT_CEN[1]+_y
            #print(_x, _y)
        #if param[0] == p and param[1]
    '''
        
    #--------------------------------------------------------
    # tmc2, tmc3, vm queue
    def connect_to_server_sub_q(self):
        sub_list = ["tmc2", "tmc3", "vm", "uploader"]
        
        sub_ObsApp_ex = [sub_list[i]+'.ex' for i in range(SUB_CNT)]
        self.consumer_sub = [None for _ in range(SUB_CNT)]
        for idx in range(SUB_CNT):
            self.consumer_sub[idx] = MsgMiddleware(self.iam, self.ics_ip_addr, self.ics_id, self.ics_pwd, sub_ObsApp_ex[idx])              
            self.consumer_sub[idx].connect_to_server()
                     
        self.consumer_sub[TMC2].define_consumer(sub_list[TMC2]+'.q', self.callback_tmc2)
        self.consumer_sub[TMC3].define_consumer(sub_list[TMC3]+'.q', self.callback_tmc3)
        self.consumer_sub[VM].define_consumer(sub_list[VM]+'.q', self.callback_vm)
        self.consumer_sub[UPLOADER].define_consumer(sub_list[UPLOADER]+'.q', self.callback_uploader)
        
        for idx in range(SUB_CNT):
            th = threading.Thread(target=self.consumer_sub[idx].start_consumer)
            th.daemon = True
            th.start()
            
    
    def callback_tmc2(self, ch, method, properties, body):
        cmd = body.decode()
        msg = "<- [TC2] %s" % cmd
        self.show_log_list(INFO, msg)
        param = cmd.split()
                
        if param[0] == HK_REQ_GETVALUE:
            self.dtvalue[self.label_list[TMC2_A]] = self.judge_value(param[1])
            self.dtvalue[self.label_list[TMC2_B]] = self.judge_value(param[2])
            self.heatlabel[self.label_list[TMC2_A]] = self.judge_value(param[3])
            self.heatlabel[self.label_list[TMC2_B]] = self.judge_value(param[4])
            
    
    def callback_tmc3(self, ch, method, properties, body):
        cmd = body.decode()
        msg = "<- [TC3] %s" % cmd
        self.show_log_list(INFO, msg)
        param = cmd.split()
                
        if param[0] == HK_REQ_GETVALUE:
            self.dtvalue[self.label_list[TMC3_B]] = self.judge_value(param[2])
            self.heatlabel[self.label_list[TMC3_B]] = self.judge_value(param[3])
            
    
    def callback_vm(self, ch, method, properties, body):
        cmd = body.decode()
        msg = "<- [VM] %s" % cmd
        if len(cmd) < 80:
            self.show_log_list(INFO, msg)
        param = cmd.split()
                    
        if param[0] == HK_REQ_GETVALUE:
            if len(param[1]) > 10 or param[1] == DEFAULT_VALUE:
                self.dpvalue = DEFAULT_VALUE
            else:
                self.dpvalue = param[1]
                
                
    def callback_uploader(self, ch, method, properties, body):
        cmd = body.decode()
        msg = "<- [UPLOADER] %s" % cmd
        self.show_log_list(INFO, msg)
        param = cmd.split()
                    
        if param[0] == IG2_HEALTH:
            self.ig2_health = int(param[1])
                   
    
    #--------------------------------------------------------
    # DC core queue
    def connect_to_server_dcs_q(self):
        dcs_list = ["DCSS", "DCSH", "DCSK"]
        
        dcs_ObsApp_ex = [dcs_list[i]+'.ex' for i in range(DC_CNT)]
        self.consumer_dcs = [None for _ in range(DC_CNT)]
        for idx in range(DC_CNT):
            self.consumer_dcs[idx] = MsgMiddleware(self.iam, self.ics_ip_addr, self.ics_id, self.ics_pwd, dcs_ObsApp_ex[idx])      
            self.consumer_dcs[idx].connect_to_server()
            
        self.consumer_dcs[SVC].define_consumer(dcs_list[SVC]+'.q', self.callback_svc)       
        self.consumer_dcs[H].define_consumer(dcs_list[H]+'.q', self.callback_h) 
        self.consumer_dcs[K].define_consumer(dcs_list[K]+'.q', self.callback_k) 

        for idx in range(DC_CNT):
            th = threading.Thread(target=self.consumer_dcs[idx].start_consumer)
            th.daemon = True
            th.start()
     
        
    def callback_svc(self, ch, method, properties, body):
        cmd = body.decode()
        msg = "<- [SVC] %s" % cmd
        self.show_log_list(INFO, msg)
        self.param_dcs[SVC] = cmd  
                
        
    def callback_h(self, ch, method, properties, body):
        cmd = body.decode()
        msg = "<- [H] %s" % cmd
        self.show_log_list(INFO, msg)
        self.param_dcs[H] = cmd  
       
        
    def callback_k(self, ch, method, properties, body):
        cmd = body.decode()
        msg = "<- [K] %s" % cmd
        self.show_log_list(INFO, msg)
        self.param_dcs[K] = cmd       
           

    #--------------------------------------------------------
    # sub process

    def judge_value(self, input):
        if input != DEFAULT_VALUE:
            value = "%.2f" % float(input)
        else:
            value = input

        return value
    
    
    def createFolder(self, dir):
        try:
            if not os.path.exists(dir):
                os.makedirs(dir)
        except OSError:
            print("Error: Creating directory. " + dir)
    
    
    def svc_progressbar_monit(self):
        #if self.svc_progressbar_start:
        #    self.svc_progressbar_start = False
            
        self.prog_timer[SVC] = QTimer(self)
        self.prog_timer[SVC].setInterval(int(self.cal_waittime[SVC]*10)) 
        self.prog_timer[SVC].timeout.connect(lambda: self.show_progressbar(SVC)) 

        self.cur_prog_step[SVC] = 0
        self.progressBar_svc.setValue(self.cur_prog_step[SVC])    
        self.prog_timer[SVC].start()  
        #print("SVC progressbar: start")
                        
            
    def hk_progressbar_monit(self):
        #if self.hk_progressbar_start:
        #    self.hk_progressbar_start = False
            
        self.prog_timer[H_K] = QTimer(self)
        self.prog_timer[H_K].setInterval(int(self.cal_waittime[H_K]*10))   
        self.prog_timer[H_K].timeout.connect(lambda: self.show_progressbar(H_K)) 
        
        self.cur_prog_step[H_K] = 0
        self.progressBar_obs.setValue(self.cur_prog_step[H_K])    
        self.prog_timer[H_K].start()
        #print("H_K progressbar: start") 
        
        self.elapsed_obs_timer = QTimer(self) 
        self.elapsed_obs_timer.setInterval(1)
        self.elapsed_obs_timer.timeout.connect(self.show_elapsed)
        
        self.measure_T = ti.time()
        self.elapsed_obs_timer.start()
            
    
    def set_fs_param(self, first=False):     
        if not self.dcss_ready:
            return

        self.acquiring[SVC] = True
        
        self.enable_dcss(False)  

        #setparam
        _exptime = float(self.e_svc_exp_time.text())
        _FS_number = int(self.e_svc_fowler_number.text())
        _fowlerTime = _exptime - T_frame * _FS_number
        self.cal_waittime[SVC] = T_br + (T_frame + _fowlerTime + (2 * T_frame * _FS_number))
                    
        self.label_svc_state.setText("Running")

        # progress bar 
        #self.svc_progressbar_start = True  
        self.svc_progressbar_monit()      
        
        if first:
            #self.cur_time = ti.time()
            
            self.dcss_setparam = True
            msg = "%s DCSS %d %.3f %d %.3f" % (CMD_SETFSPARAM_ICS, self.simulation, _exptime, _FS_number, _fowlerTime)
            #print(_exptime, _FS_number)
        else:
            #print(ti.time() - self.cur_time)
            msg = "%s DCSS %d 0" % (CMD_ACQUIRERAMP_ICS, self.simulation)
        self.publish_to_queue(msg)

        
    def abort_acquisition(self):
        if self.cur_prog_step[SVC] > 0:
            self.prog_timer[SVC].stop()
              
        msg = "%s DCSS %d" % (CMD_STOPACQUISITION, self.simulation)
        self.publish_to_queue(msg)  
    
    
    
    #data load for observation from DCSS
    def load_data(self, folder_name):
        
        self.label_svc_state.setText("Transfer")
        
        try:
            self.fitsfullpath = "%sObsApp/dcss/Fowler/%s" % (WORKING_DIR, folder_name)

            hdul = fits.open(self.fitsfullpath)
            msg = "%.5f" % (ti.time() - self.NFS_load_time)
            self.show_log_list(INFO, msg)
            
            data = hdul[0].data
            self.svc_header = hdul[0].header
            _img = np.array(data, dtype = "f")
            hdul.close()
            
            #_img = np.rot90(_img, 1)
            self.svc_img = self.slit_image_flip_func(_img)
            #self.svc_img = rotate(_svc_img, -45, axes=(1,0), reshape=None)      
                        
            self.draw = True
            
            ny, nx = self.svc_img.shape
            self.svc_img_cut = self.svc_img[self.svc_cut_y:ny-self.svc_cut_y, self.svc_cut_x:nx-self.svc_cut_x] 
            self.image_display(self.svc_img_cut)
            
            self.update_sw_offset(self.svc_img, self.mask)
        
            self.label_svc_state.setText("Idle")

        except:
            self.svc_img = None
            self.show_log_list(WARNING, "No image")            
        
        
    def image_display(self, imgdata, new = True):
        self.zmin, self.zmax = zs.zscale(imgdata)
        range = "%d ~ %d" % (self.zmin, self.zmax)
        
        self.label_zscale.setText(range)
        #self.mmin, self.mmax = np.min(imgdata), np.max(imgdata)
        self.e_mscale_min.setText("%.1f" % self.mmin)
        self.e_mscale_max.setText("%.1f" % self.mmax)
            
        #if self.chk_autosave.isChecked():
        #    self.save_fits(dc_idx)
        
        #if self.svc_mode == GUIDE_MODE:    
        if self.cur_frame == A_BOX:
            self.guide_x, self.guide_y = self.A_x, self.A_y
        elif self.cur_frame == B_BOX:
            self.guide_x, self.guide_y = self.B_x, self.B_y   
        elif self.cur_frame == OFF_BOX:
            self.guide_x, self.guide_y = self.off_x, self.off_y
        #else:
        #    self.guide_x, self.guide_y= self.A_x, self.A_y
                
        if new and self.display_click(self.guide_x, self.guide_y):
            self.find_center = True
        else:
            self.find_center = False
            
        self.reload_img(imgdata)   
        
        
    def display_click(self, x_pos, y_pos):
        
        cen_x_in, cen_y_in, ret = self.calc_offset(int(x_pos), int(y_pos))
        
        if ret:
            self.draw_zoomin(self.cropdata, x_pos, y_pos, cen_x_in, cen_y_in)
            self.show_GaussianFitting()
            
        return ret
    
    
    def calc_offset(self, x_pos, y_pos):
        ret = False
        
        if (x_pos < 0) | (y_pos < 0): 
            return 0, 0, ret
        if self.svc_img is None: 
            return 0, 0, ret
        # make croped data
        ny, nx = self.svc_img.shape

        y1 = np.max([0, y_pos - ZOOMW]) 
        y2 = np.min([ny, y_pos + ZOOMW]) 
        x1 = np.max([0, x_pos - ZOOMW]) 
        x2 = np.min([nx, x_pos + ZOOMW]) 
        
        self.cropdata = self.svc_img[y1:y2, x1:x2]

        self.cropmask = self.mask[y1:y2, x1:x2]

        # display pixel value and define click point in the crop image coordinate
        try:
            self.height, cen_x_in, cen_y_in, self.sigma, self.background = self.FindingCentroid(self.cropdata, self.cropmask)
            #self.height_iMM = self.height
            
            msg = "Gaussian param P:%.0f B:%.0f X:%.1f Y:%.1f \nFWHM:%.2f" % (self.height, self.background, cen_x_in, cen_y_in, self.sigma*2.35482)
            self.show_log_list(INFO, msg)
            
            ret = True

            if not (np.isfinite(cen_x_in) and np.isfinite(cen_y_in)):
                cen_x_in, cen_y_in = x_pos - x1, y_pos - y1

        except Exception as e:
            import traceback, sys
            traceback.print_exc(file=sys.stdout)

            cen_x_in, cen_y_in = x_pos - x1, y_pos - y1

        # change coordinate for the full image
        self.cen_x = cen_x_in + x1
        self.cen_y = cen_y_in + y1
        
        return cen_x_in, cen_y_in, ret
    
    
    #sky, mask        
    def reload_img(self, imgdata, left_click=False):
        
        #if not self.img_draw: 
        #    return
        
        #self.img_draw = False
        #imgdata = self.img_buffer
        
        self.clean_ax(self.image_ax[IMG_SVC])
        
        try:
            # main draw                            
            _min, _max = 0, 0
            if self.radio_zscale.isChecked():
                _min, _max = self.zmin, self.zmax
            elif self.radio_mscale.isChecked():
                self.mmin, self.mmax = float(self.e_mscale_min.text()), float(self.e_mscale_max.text())
                _min, _max = self.mmin, self.mmax
                            
            self.display_coordinate(self.image_ax[IMG_SVC], imgdata, _min, _max, self.PA)
            if self.chk_off_slit.isChecked():
                self.display_box(self.image_ax[IMG_SVC], self.off_x, self.off_y, OFF_BOX_CLR)
            
            self.display_box(self.image_ax[IMG_SVC], self.A_x, self.A_y, A_BOX_CLR)
            self.display_box(self.image_ax[IMG_SVC], self.B_x, self.B_y, B_BOX_CLR)
            
            if left_click:
                self.display_box(self.image_ax[IMG_SVC], self.click_x, self.click_y, BOX_CLR) 
                
            self.image_canvas[IMG_SVC].draw()
                
        except:
            pass
                
        
    def display_coordinate(self, imageax, imgdata, vmin, vmax, pa_tel):
        imageax.clear()  #20231005
        imageax.imshow(imgdata, vmin=vmin, vmax=vmax, cmap='gray', origin='lower')
                            
        imageax.axis('off')
        
        imageax.set_xlim(0, SVC_FRAME_X-self.svc_cut_x*2)
        imageax.set_xlim(0, SVC_FRAME_Y-self.svc_cut_y*2)
        
        if not self.chk_view_drawing.isChecked():
            return
        
        cx, cy = 250, SVC_FRAME_Y-self.svc_cut_y*2-200
        arrow_size = 100
        text_ratio = 2
        
        PA = pa_tel + PQ_ROT
        s_color = "limegreen"
        u, v = (arrow_size*np.sin(np.deg2rad(PA)), arrow_size*np.cos(np.deg2rad(PA)))
        imageax.arrow(cx, cy, u, v, color=s_color, width=2, head_width=20)
        imageax.text(cx+u*text_ratio-40, cy+v*text_ratio*0.8, "N", color=s_color, size=10)
        PA = PA - 90
        u, v = (arrow_size*np.sin(np.deg2rad(PA)), arrow_size*np.cos(np.deg2rad(PA)))
        imageax.arrow(cx, cy, u, v, color=s_color, width=2, head_width=20)
        imageax.text(cx+u*text_ratio-10, cy+v*text_ratio-30, "E", color=s_color, size=10)
        
        cx = SVC_FRAME_X-self.svc_cut_x*2-250 + 140
        cy = SVC_FRAME_Y-self.svc_cut_y*2-200 + 20

        PA = PQ_ROT + 180
        u, v = (arrow_size*np.sin(np.deg2rad(PA)), arrow_size*np.cos(np.deg2rad(PA)))
        imageax.arrow(cx, cy, u, v, color=s_color, width=2, head_width=20)
        imageax.text(cx+u*text_ratio-60, cy+v*text_ratio*0.8, "+p", color=s_color, size=10)
        #print(cx, cy, u, v, cx+u*text_ratio-60, cy+v*text_ratio*0.8)
        PA = PA + 90
        u, v = (arrow_size*np.sin(np.deg2rad(PA)), arrow_size*np.cos(np.deg2rad(PA)))
        imageax.arrow(cx, cy, u, v, color=s_color, width=2, head_width=20)
        imageax.text(cx+u*text_ratio*1.2, cy+v*text_ratio-30, "+q", color=s_color, size=10)

        '''
        PA = 0
        u, v = (50*np.sin(np.deg2rad(PA)), 50*np.cos(np.deg2rad(PA)))
        imageax.arrow(cx, cy, u, v, color="cyan", width=1.5, head_width=12)
        imageax.text(cx+u*1.8, cy+v*1.8, "Y", color="cyan", size=10)
        PA = PA + 90
        u, v = (50*np.sin(np.deg2rad(PA)), 50*np.cos(np.deg2rad(PA)))
        imageax.arrow(cx, cy, u, v, color="cyan", width=1.5, head_width=12)
        imageax.text(cx+u*1.8, cy+v*1.8, "X", color="cyan", size=10)
        '''
        
        
    def display_box(self, ax, x, y, boxcolor):
        ax.plot(SLIT_CEN[0] - self.svc_cut_x, SLIT_CEN[1] - self.svc_cut_y, "P", color="limegreen", ms=7)
        
        if not self.chk_view_drawing.isChecked():
            return
        
        if not (np.isfinite(x) and np.isfinite(x)):
            msg = "Invalid Value indisplay specialbox:", x, y
            self.logger.error(msg)
            return

        if (int(x) == 0 and int(y) == 0):
            return

        x_pos, y_pos = (int(x)-self.svc_cut_x, int(y)-self.svc_cut_x)

        zbox = Rectangle( (x_pos-ZOOMW, y_pos-ZOOMW), 2*ZOOMW, 2*ZOOMW, facecolor='none', edgecolor=boxcolor)
        ax.add_patch(zbox)

        ax.plot([x_pos-ZOOMW+5,x_pos+ZOOMW], [y_pos, y_pos], color=boxcolor)
        ax.plot([x_pos, x_pos], [y_pos-ZOOMW,y_pos+ZOOMW-5], color=boxcolor)
    
    
    
    # FITTING_2D_MASK from original IGRINS
    def FindingCentroid(self, imgdata, mask): 

        height, sx, sy, sigma , background= (0, 0, 0, 0, 0)

        if self.fwhm_mode == FWHM_FIX:
            fit_gaussian_func = tmcfmask.fitgaussian2d_mask_with_saturation_fixed_width
            fwhm_width = self.fwhm_mode_value / PIXELSCALE / 2.35
            params = fit_gaussian_func(imgdata, mask > 0, width=fwhm_width)
        else:
            if self.fwhm_mode == FWHM_GUESS:
                params = tmcfmask.fitgaussian2d_mask_with_saturation(imgdata, mask>0, fit_width=False)
            else:
                params = tmcfmask.fitgaussian2d_mask_with_saturation(imgdata, mask>0, fit_width=True)
        # fit_gaussian_func = tmcfmask.fitgaussian2d_mask_with_saturation_fixed_width
        # params = fit_gaussian_func(data, mask>0, width=4.)
        if params != None:  #20231007
            height, sx, sy, sigma, background = params[0], params[1], params[2], params[3], params[4]

        return height, sx, sy, sigma, background
        
        
    def draw_zoomin(self, cropdata, x_pos, y_pos, x_source_crop, y_source_crop):
        
        self.clean_ax(self.image_ax[IMG_EXPAND])
        self.clean_ax(self.image_ax[IMG_FITTING], False)
        
        try:                                
            # zoomin draw    
            _min, _max = 0, 0        
            if self.radio_zscale.isChecked():
                _min, _max = self.zmin, self.zmax
            elif self.radio_mscale.isChecked():
                _min, _max = self.mmin, self.mmax
                
            self.image_ax[IMG_EXPAND].axis('off')
            self.image_ax[IMG_EXPAND].clear()  #20231005
            self.image_ax[IMG_EXPAND].imshow(cropdata, vmin=_min, vmax=_max, cmap='gray', origin='lower')
            
            strtmp = 'X:%6.1f  Y:%6.1f \nH:%.0f S:%.2f B:%.0f' % (x_pos, y_pos, self.height, self.sigma, self.background)
            self.image_ax[IMG_EXPAND].text(0.5, +0.3, strtmp, \
                            color='red', ha='center', va='top', \
                            transform=self.image_ax[IMG_EXPAND].transAxes, fontsize=8)
            ny, nx = cropdata.shape
            self.image_ax[IMG_EXPAND].plot([(nx-1)/2,(nx-1)/2], [0, ny], '-', color='yellow')
            self.image_ax[IMG_EXPAND].plot([0, nx], [(ny-1)/2,(ny-1)/2], '-', color='yellow')
            
            # draw a mark in zoom-in
            if 0 <= x_source_crop <= ZOOMW*2 and 0 <= y_source_crop <= ZOOMW*2:
                _circle = Circle( (x_source_crop, y_source_crop), \
                                facecolor='none', edgecolor='blue',
                                radius=self.sigma * 2.35 / 2.)
                self.image_ax[IMG_EXPAND].add_patch(_circle)
            
            self.image_canvas[IMG_EXPAND].draw()
                            
        except:
            pass

            
    
    def clean_ax(self, ax, ticks_off = True):
        ax.cla()
        if (ticks_off == True):
            ax.set_xticklabels([])
            ax.set_yticklabels([])

            ax.set_frame_on(False)
            ax.set_xticks([])
            ax.set_yticks([])
            
            
    def show_GaussianFitting(self):
        if self.fitting_clicked:
            self.clean_ax(self.image_ax[IMG_FITTING], ticks_off = False)
            self.contour_plot()

        else:
            self.clean_ax(self.image_ax[IMG_FITTING], ticks_off = False)
            self.radial_fits()
            
    
    def radial_fits(self):
        try:
            if (np.isnan(self.cen_x) or np.isnan(self.cen_y)):
                DOFIT = False
                return 0
            
            if not self.draw:
                return 0                
            
            DOFIT = True

            (ny, nx) = self.svc_img.shape
            y1 = np.max([0, self.cen_y - CONTOURW])
            y2 = np.min([ny, self.cen_y + CONTOURW])
            x1 = np.max([0, self.cen_x - CONTOURW])
            x2 = np.min([nx, self.cen_x + CONTOURW])
            # make data array

            data = self.svc_img[int(y1):int(y2), int(x1):int(x2)]
            cen_x_in, cen_y_in = (self.cen_x - x1, self.cen_y - y1)

            # matplotlib part
            if cen_x_in == 0 and cen_y_in == 0:
                cen_x_in = ZOOMW
                cen_y_in = ZOOMW
                DOFIT = False

            # Plot the sampled data from the selected source
            radialprofile = self.radial_profile(data, cen_x_in, cen_y_in)
            self.image_ax[IMG_FITTING].plot(radialprofile, "r.", markersize=7)

            if DOFIT == True :
            # Now, prepare for fitting process
                arrsize = radialprofile.size
                xarr = np.arange(-arrsize + 1, arrsize)
                doubleprofile = np.concatenate((radialprofile[:0:-1], radialprofile))

            # Do the 1-d gaussian fitting
            # Initial guess value(optional)
            #  params = [background, Amplitude, Xcenter, width]
            #  params = [5000, 3000, 0, 3] would be good initial guess
                #gfit = gf.onedgaussfit(xarr, doubleprofile)
                gfit = self.onedgaussfit(xarr, doubleprofile)
                #print(gfit)

            # Put the fitted values to each separate variables
                amplitude = gfit[0]
                bkground = gfit[1]
                xcenter = gfit[2]
                sigma = abs(gfit[3])
                self.fwhm = 2.3548*sigma  # FWHM is width measured at 1/2 peak.

            # Generate gaussian profile with fitted parameters for plotting
                xfit = np.arange(-arrsize + 1, arrsize, 0.1)
                yfit = self.gaussian(xfit, amplitude, bkground, xcenter, sigma)
                self.image_ax[IMG_FITTING].plot(xfit, yfit, "b-")

            else:
                bkground = 0.0
                amplitude = 0.0
                xcenter = 0.0
                sigma = 0.0
                self.fwhm = sigma

            self.image_ax[IMG_FITTING].set_xlim(-0.5, 15)
            self.image_ax[IMG_FITTING].set_frame_on(True)
            self.image_ax[IMG_FITTING].tick_params(direction='in')
            self.image_ax[IMG_FITTING].ticklabel_format(axis='y',style='sci')
            self.image_ax[IMG_FITTING].set_aspect('auto','datalim')

            xcen_info = "Xc: %5.1f" % (self.cen_x)
            ycen_info = "Yc: %5.1f" % (self.cen_y)
            fwhm_info = "FWHM: %4.2fpix(%5.2f\")"\
                    % (self.fwhm, self.fwhm*PIXELSCALE)
            peak_info = "Peak: %6.1fADU" % (amplitude)
            self.image_ax[IMG_FITTING].text(0.6,+0.5,('%s,%s\n%s\n%s') % (xcen_info, ycen_info, fwhm_info, peak_info), color='black', ha='center',va='bottom',\
                                transform=self.image_ax[IMG_FITTING].transAxes, fontsize=7)

            self.image_canvas[IMG_FITTING].draw()
        
        except ZeroDivisionError:
            pass
        except ValueError:
            pass
        except Exception as e:
            import traceback, sys
            traceback.print_exc(file=sys.stdout)
        
    
    def radial_profile(self, image, xcen, ycen):
        y, x = np.indices(image.shape)
        r = np.sqrt( (x - xcen)**2 + (y - ycen)**2 )
        ind = np.argsort(r.flat)

        sr = r.flat[ind]
        sim = image.flat[ind]
        ri = sr.astype(int)

        deltar = ri[1:] - ri[:-1]
        rind = np.where(deltar)[0]
        nr = rind[1:] - rind[:-1]
        csim = np.cumsum(sim, dtype = np.float64)
        tbin = csim[rind[1:]] - csim[rind[:-1]]
        profile = tbin/nr

       # Add 0-th value to the array
        radialprofile = np.concatenate((np.array([image[int(ycen), int(xcen)]]),
                                        profile))

        return radialprofile
        
        
    def onedgaussfit(self, xcoord, intensity):
        coeff, pcov = curve_fit(self.gaussian, xcoord, intensity)
        return coeff
    
    
    # gaussian function for gaussian plot
    def gaussian(self, x, amplitude, background, xcenter, width):
        coeff = amplitude
        idx = (x - xcenter)**2 / (2.*width**2)
        body = np.exp(-idx)
        
        return (coeff*body) + background
    
    
    def contour_plot(self, x_cen=0, y_cen=0):
        try:
            if (np.isnan(self.cen_x) or np.isnan(self.cen_y)):
                DOFIT = False
                return 0
            
            if not self.draw:
                return 0 
            
            (ny, nx) = self.svc_img.shape
            y1 = int(np.max([0, self.cen_y - CONTOURW]))
            y2 = int(np.min([ny, self.cen_y + CONTOURW]))
            x1 = int(np.max([0, self.cen_x - CONTOURW]))
            x2 = int(np.min([nx, self.cen_x + CONTOURW]))

            contourdata = self.svc_img[y1:y2, x1:x2]
            # crop the image nearby source

            # contour level correction
            cmin, cmax = zs.zscale(contourdata)
            #cmin = self.zmin
            #cmax = np.max(contourdata)
            # clevel = np.arange(cmin,cmax*1.2,int((cmax-cmin)/15))[2:]
            clevel = np.linspace(cmin,cmax*1.2, 15)[2:]

            scontour = self.image_ax[IMG_FITTING].contour(contourdata, levels=clevel)

            scontour.set_clim(self.zmin, self.zmax)
            self.image_ax[IMG_FITTING].set_aspect('equal','datalim')

            self.image_ax[IMG_FITTING].set_frame_on(True)
            strtmp = "X=%6.1f Y=%6.1f" % (self.cen_x, self.cen_y)
            self.image_ax[IMG_FITTING].text(0.5, +0.95, strtmp, \
            color='black', ha='center', va='top', \
            transform=self.image_ax[IMG_FITTING].transAxes, fontsize=8)
            
            self.image_canvas[IMG_FITTING].draw()
        
        except ZeroDivisionError:
            pass
        except ValueError:
            pass
        except Exception as e:
            import traceback, sys
            traceback.print_exc(file=sys.stdout)
            
    
    #--------------------------------------------------------
    # gui set
    def QShowValue(self, widget, label):
        value = self.dtvalue[label]
        name = "Det %s" % self.key_to_label[label][3:].upper()
        
        prev_sts = self.det_sts[label]
        
        if float(self.temp_lower_normal[label]) <= float(value) <= float(self.temp_upper_normal[label]):
            self.QWidgetLabelColor(widget, "green")
            msgbar = None
            
            self.det_sts[label] = "good"
        
        else:
            color = None
            if value == DEFAULT_VALUE:
                color = "dimgray"
                msgbar = "%s is ERROR!!!" % name        
                self.det_sts[label] = "error"
                
            elif float(self.temp_lower_warning[label]) <= float(value) <= float(self.temp_upper_warning[label]):
                color = "gold"
                msgbar = "%s temperature WARNNING!!!" % name
                self.det_sts[label] = "warn"
                
            elif float(self.temp_upper_warning[label]) < float(value):
                color = "red"
                msgbar = "%s temperature is too high!!!" % name
                self.det_sts[label] = "fatal"
                
            elif float(self.temp_lower_warning[label]) > float(value):
                color = "red"
                msgbar = "%s temperature is too low!!!" % name
                self.det_sts[label] = "fatal"
                
            self.QWidgetLabelColor(widget, color)
            self.QWidgetLabelColor(self.label_messagebar, color)
            
        widget.setText(value)
        self.label_messagebar.setText(msgbar)
        if prev_sts != self.det_sts[label]:
            self.show_log_list(INFO, msgbar)
        
    
    def QWidgetLabelColor(self, widget, textcolor, bgcolor=None):
        if bgcolor == None:
            label = "QLabel {color:%s}" % textcolor
            widget.setStyleSheet(label)
        else:
            label = "QLabel {color:%s;background:%s}" % (textcolor, bgcolor)
            widget.setStyleSheet(label)
            
            
    def QWidgetBtnColor(self, widget, textcolor, bgcolor=None):
        if bgcolor == None:
            label = "QPushButton {color:%s}" % textcolor
            widget.setStyleSheet(label)
        else:
            label = "QPushButton {color:%s;background:%s}" % (textcolor, bgcolor)
            widget.setStyleSheet(label)
            
            
    def widget_resize(self, cur_width, cur_height, widget, init_idx):
        is_rect = widget.geometry()        
        init_rect = self.init_widget_rect[init_idx]
        
        new_rect_left = np.rint((is_rect.left() * cur_width) / self.prev_rect.width())
        new_rect_top = np.rint((is_rect.top() * cur_height) / self.prev_rect.height())
        new_rect_width = np.rint((is_rect.width() * cur_width) / self.prev_rect.width())
        new_rect_height = np.rint((is_rect.height() * cur_height) / self.prev_rect.height())
        
        if new_rect_width >= init_rect.width() or new_rect_height >= init_rect.height():
            widget.setGeometry(new_rect_left, new_rect_top, new_rect_width, new_rect_height)
        else:
            widget.setGeometry(init_rect.left(), init_rect.top(), init_rect.width(), init_rect.height())
        
        self.prev_widget_rect[init_idx] = init_rect
        
        
    def show_log_list(self, log_option, msg):
        if self.radio_show_loglist.isChecked():
            if self.listWidget_log.count() >= 40:
                self.listWidget_log.takeItem(0)
            self.listWidget_log.addItem(msg)
            
        self.log.send(self.iam, log_option, msg)
        
        
    def move_to_telescope(self, dp, dq, mode=ACQ_MODE):
        msg = "%s %.3f %.3f %d" % (OBSAPP_CAL_OFFSET, dp, dq, mode)
        self.publish_to_queue(msg) 


    # unit pixel -> arcsec
    def calc_xy_to_pq(self, para1, para2, opposite=False):    # x-y => p-q               
        PA = SLIT_ANG
        if opposite:
            #PA *= (-1)
            _p, _q = para1, para2
            dx = - ( _q*np.cos(np.deg2rad(PA)) - _p*np.sin(np.deg2rad(PA)) ) / PIXELSCALE
            dy = ( _q*np.sin(np.deg2rad(PA)) + _p*np.cos(np.deg2rad(PA)) ) / PIXELSCALE
            return dx, dy
        else: 
            _x, _y = para1, para2
            _q = - ( _x*np.cos(np.deg2rad(PA)) - _y*np.sin(np.deg2rad(PA)) ) * PIXELSCALE
            _p = - ( _x*np.sin(np.deg2rad(PA)) + _y*np.cos(np.deg2rad(PA)) ) * PIXELSCALE
            return _p, _q
        
    
    #--------------------------------------------------------
    # button, event
    
    def resizeEvent(self, event: QResizeEvent) -> None:
        
        if not self.resize_enable:
            return
        
        cur_width = event.size().width()
        cur_height = event.size().height()
        
        if cur_width < self.min_rect.width() or cur_height < self.min_rect.height():
            self.setGeometry(QRect(0, 0, self.min_rect.width(), self.min_rect.height()))
            return

        self.widget_resize(cur_width, cur_height, self.groupBox_InstrumentStatus, GROUPBOX_IS)   
        self.widget_resize(cur_width, cur_height, self.groupBox_ScienceObservation, GROUPBOX_SO)
        
        self.widget_resize(cur_width, cur_height, self.frame_expand, FRM_EXPAND)
        self.widget_resize(cur_width, cur_height, self.frame_fitting, FRM_FITTING)
        self.widget_resize(cur_width, cur_height, self.frame_svc, FRM_SVC)
        
        self.widget_resize(cur_width, cur_height, self.groupBox_profile, GROUPBOX_PROFILE)
        self.widget_resize(cur_width, cur_height, self.frame_profile, FRM_PROFILE)
        self.widget_resize(cur_width, cur_height, self.label_slit, LABEL_SLIT)
        self.widget_resize(cur_width, cur_height, self.label_star, LABEL_STAR)
        self.widget_resize(cur_width, cur_height, self.label_star_slit, LABEL_SLITSTAR)
        self.widget_resize(cur_width, cur_height, self.label_sw_slit, SW_LABEL_SLIT)
        self.widget_resize(cur_width, cur_height, self.label_sw_star, SW_LABEL_STAR)
        self.widget_resize(cur_width, cur_height, self.label_sw_star_slit, SW_LABEL_SLITSTAR)
        
        self.widget_resize(cur_width, cur_height, self.groupBox_SlitViewCamera, GROUPBOX_SVC)
        self.widget_resize(cur_width, cur_height, self.groupBox_zscale, GROUPBOX_SCALE)
        
        self.widget_resize(cur_width, cur_height, self.label_messagebar, LABEL_MSG)
        
        self.widget_resize(cur_width, cur_height, self.radio_none, SEL_NONE)
        self.widget_resize(cur_width, cur_height, self.radio_show_logfile, SEL_LOGFILE)
        self.widget_resize(cur_width, cur_height, self.radio_show_loglist, SEL_LOGLIST)
        
        self.widget_resize(cur_width, cur_height, self.listWidget_log, LIST_LOG)

        self.prev_rect = self.geometry()
        
        return super().resizeEvent(event)    

    
    def image_leftclick(self, event):
        if event.xdata == None or event.ydata == None:
            return
        
        #print("Press (frame):", event.xdata, event.ydata)
        #print("self.prev_widget_rect[FRM_SVC]: ", self.prev_widget_rect[FRM_SVC])
        self.click_x = event.xdata + self.svc_cut_x
        self.click_y = event.ydata + self.svc_cut_y
        #print("Press (svc):", self.click_x, self.click_y)
        
        click_p, click_q = self.calc_xy_to_pq(self.click_x-SLIT_CEN[0], self.click_y-SLIT_CEN[1])
        #print("Press (p-q):", click_p, click_q)
        
        if self.display_click(self.click_x, self.click_y):
            self.find_center = True
        else:
            self.find_center = False
            
        self.reload_img(self.svc_img_cut, True)
                
                
    def fitting_leftclick(self, event):
        if self.fitting_clicked:
            self.fitting_clicked = False
        else:
            self.fitting_clicked = True
            
        self.show_GaussianFitting()
        
            
    def set_continue_mode(self):
        if self.chk_continue.isChecked():
            self.svc_mode = CONT_MODE
            self.stop_clicked = False
        else:
            self.svc_mode = SINGLE_MODE
            self.stop_clicked = True
            
            
    def status_iamge_taking(self, start):
        msg = "%s %d" % (OBSAPP_TAKING_IMG, start)
        self.publish_to_queue(msg)
        

    def single(self):
        
        if self.svc_mode == GUIDE_MODE:
            return
        
        if self.bt_single.text() == "Exposure":
            if self.svc_mode == CONT_MODE:
                self.bt_single.setText("Stop")                
                self.stop_clicked = False
                self.status_iamge_taking(True)
            else:
                self.bt_single.setText("Abort")
                
            self.QWidgetBtnColor(self.bt_single, "yellow", "blue")
            self.set_fs_param(True)
            
            self.bt_slow_guide.setEnabled(False)
            
        else:       
            if self.svc_mode == CONT_MODE:     
                self.stop_clicked = True   
                self.status_iamge_taking(False)
            else:
                self.abort_acquisition()       
            
            self.bt_single.setText("Exposure")  
            
            self.bt_slow_guide.setEnabled(True)
    
    
    def auto_save_image(self):
        if self.chk_auto_save.isChecked():
            self.e_saving_number.setEnabled(True)
            self.e_repeat_file_name.setEnabled(False)
            self.bt_repeat_filesave.setEnabled(False)
        else:
            self.e_saving_number.setEnabled(False)
            self.e_repeat_file_name.setEnabled(True)
            self.bt_repeat_filesave.setEnabled(True)
            
            
    def change_outoufnumber_svc(self):
        self.out_of_number_svc = int(self.e_saving_number.text())
        msg = "%s %d" % (OBSAPP_OUTOF_NUMBER_SVC, self.out_of_number_svc)
        self.publish_to_queue(msg)
        
        
    def manual_filesave(self):        
        if self.fitsfullpath == None:
            return
       
        foldername = ti.strftime("%02Y%02m%02d/", ti.localtime()) 
        self.createFolder(self.svc_path + foldername)
        
        newfile = self.svc_path + foldername + self.e_repeat_file_name.text()
        if not ".fits" in newfile:
            newfile += ".fits"
        copyfile(self.fitsfullpath, newfile)
        
        #msg = "%s %s" % (OBSAPP_SAVE_SVC, self.file_name)
        #self.publish_to_queue(msg)
        
        self.fitsfullpath = None

    
    def set_center(self):
        dx = self.click_x - SLIT_CEN[0]
        dy = self.click_y - SLIT_CEN[1]
        
        if dx == 0 and dy == 0:
           return
        
        #pixel -> arcsec
        #print("set_senter (dx, dy):", dx, dy)
        dp, dq = self.calc_xy_to_pq(dx, dy)   
        #print("set_senter (dp, dq):", dp, dq)
        #dra, ddec = self.calc_pq_to_radec(dp, dq)
        self.move_to_telescope(dp, dq)
    
    
    def set_off_slit(self):
        if self.chk_off_slit.isChecked():
            self.prev_frame = self.cur_frame
            self.cur_frame = OFF_BOX
        else:
            self.cur_frame = self.prev_frame
            
        self.clean_ax(self.image_ax[IMG_SVC])
        self.bt_set_guide_star.setEnabled(self.chk_off_slit.isChecked())
        if self.chk_off_slit.isChecked():
            self.display_box(self.image_ax[IMG_SVC], self.off_x, self.off_y, OFF_BOX_CLR)
                  
        self.reload_img(self.svc_img_cut)
    
    
    def set_guide_star(self):
        self.off_x, self.off_y = self.click_x, self.click_y
        self.set_off_slit()
        
        
    #p, q coordiation!!!!
    def move_p(self, negative): #+:True, -:Minus 
        dp = float(self.e_offset.text())
        #20231003
        if negative:
            dp *= (-1)
        #print("move P:", dp) 
        self.move_to_telescope(dp, 0)
        
    
    #p, q coordiation!!!!
    def move_q(self, positive): #+:True, -:Minus 
        dq = float(self.e_offset.text())
        if not positive:
            dq *= (-1)
         
        #print("move q:", dq)  
        self.move_to_telescope(0, dq)
        
    
    
    def slow_guide(self):
                
        self.svc_mode = GUIDE_MODE
        
        if self.bt_slow_guide.text() == "Slow Guide":
            
            self.cur_guide_cnt = 0 
            self.label_cur_Idx.setText("0 /")
            
            self.center_ra = []
            self.center_dec = []
                            
            self.bt_slow_guide.setText("Slow Guide Stop")
            self.stop_clicked = False
            
            self.QWidgetBtnColor(self.bt_slow_guide, "yellow", "blue")
            self.set_fs_param(True)
            
            self.bt_single.setEnabled(False)
            self.QWidgetBtnColor(self.bt_single, "silver")
            
            self.status_iamge_taking(True)
            
        else:
            self.bt_slow_guide.setText("Slow Guide") 
            self.stop_clicked = True
            
            self.bt_single.setEnabled(True)
            self.QWidgetBtnColor(self.bt_single, "black")
            
            self.status_iamge_taking(False)
            
        
    def view_drawing(self):
        self.reload_img(self.svc_img_cut)
            
            
    def select_raw(self):
        self.image_display(self.svc_img_cut)
    
    
    def select_sub(self):
        #20231007
        if self.sky_exp_time <= 0:
            return
        
        cor = float(self.e_svc_exp_time.text()) / self.sky_exp_time
        imgSub_data = self.svc_img - self.sky_data*cor
        
        ny, nx = imgSub_data.shape
        
        imgSub_data_cut = imgSub_data[self.svc_cut_y:ny-self.svc_cut_y, self.svc_cut_x:nx-self.svc_cut_x]
        
        self.image_display(imgSub_data_cut, False)

    
    def mark_sky(self):
        # data copy?
        
        # read image and exposure time
        self.sky_data = self.svc_img
        self.sky_exp_time = float(self.svc_header["EXPTIME"])
        

    def select_zscale(self):
        self.reload_img(self.svc_img_cut)


    def select_mscale(self):
        self.mmin, self.mmax = float(self.e_mscale_min.text()), float(self.e_mscale_max.text())
        self.reload_img(self.svc_img_cut)
    
    
    def select_log_none(self):
        self.resize_enable = False
        
        self.radio_none.setChecked(True)
        self.radio_show_logfile.setChecked(False)
        self.radio_show_loglist.setChecked(False)
        
        self.setGeometry(QRect(0, 0, 870, 662))
        self.reset_resize()
            
    
    def select_log_file(self):
        self.resize_enable = False
        
        self.radio_none.setChecked(False)
        self.radio_show_logfile.setChecked(True)
        self.radio_show_loglist.setChecked(False)
        
        self.setGeometry(QRect(0, 0, 870, 662))
        self.reset_resize()
    
        # show log file
        logpath = WORKING_DIR + self.iam + '/Log/' + ti.strftime("%Y%m%d", ti.localtime())+".log"
        subprocess.Popen(['xdg-open', logpath])
        
        
    def select_log_list(self):
        self.resize_enable = False
        
        self.radio_none.setChecked(False)
        self.radio_show_logfile.setChecked(False)
        self.radio_show_loglist.setChecked(True)
        
        #self.editlist_loglist.clear()
        
        # show listview
        self.setGeometry(QRect(0, 0, 1211, 662))     
        self.reset_resize()
        
        
    def reset_resize(self):
        self.min_rect = self.geometry()
        self.prev_rect = self.min_rect
        #print(self.min_rect)
        
        self.init_widget_rect[GROUPBOX_IS] = self.groupBox_InstrumentStatus.geometry()      # GROUPBOX_IS       
        self.init_widget_rect[GROUPBOX_SO] = self.groupBox_ScienceObservation.geometry()    # GROUPBOX_SO
        
        self.init_widget_rect[GROUPBOX_PROFILE] = self.groupBox_profile.geometry()          # GROUPBOX_PROFILE
        self.init_widget_rect[FRM_PROFILE] = self.frame_profile.geometry()                  # FRM_PROFILE
        
        self.init_widget_rect[LABEL_SLIT] = self.label_slit.geometry()                   # LABEL_SLIT
        self.init_widget_rect[LABEL_STAR] = self.label_star.geometry()                   # LABEL_STAR
        self.init_widget_rect[LABEL_SLITSTAR] = self.label_star_slit.geometry()               # LABEL_SLITSTAR
        self.init_widget_rect[SW_LABEL_SLIT] = self.label_sw_slit.geometry()                # SW_LABEL_SLIT
        self.init_widget_rect[SW_LABEL_STAR] = self.label_sw_star.geometry()                # SW_LABEL_STAR
        self.init_widget_rect[SW_LABEL_SLITSTAR] = self.label_sw_star_slit.geometry()            # SW_LABEL_SLITSTAR
        
            
        self.init_widget_rect[FRM_EXPAND] = self.frame_expand.geometry()                    # FRM_EXPAND
        self.init_widget_rect[FRM_FITTING] = self.frame_fitting.geometry()                  # FRM_FITTING
        self.init_widget_rect[FRM_SVC] = self.frame_svc.geometry()                          # FRM_SVC
            
        self.init_widget_rect[GROUPBOX_SVC] = self.groupBox_SlitViewCamera.geometry()       # GROUPBOX_SVC
        self.init_widget_rect[GROUPBOX_SCALE] = self.groupBox_zscale.geometry()             # GROUPBOX_SCALE
        self.init_widget_rect[LABEL_MSG] = self.label_messagebar.geometry()                 # LABEL_MSG
        
        self.init_widget_rect[SEL_NONE] = self.radio_none.geometry()                        # SEL_NONE
        self.init_widget_rect[SEL_LOGFILE] = self.radio_show_logfile.geometry()             # SEL_LOGFILE
        self.init_widget_rect[SEL_LOGLIST] = self.radio_show_loglist.geometry()             # SEL_LOGLIST
        self.init_widget_rect[LIST_LOG] = self.listWidget_log.geometry()                  # LIST_LOG
        
        self.prev_widget_rect = self.init_widget_rect
        
        self.resize_enable = True
        
     
    
    def show_progressbar(self, dc_idx):
        if self.cur_prog_step[dc_idx] >= 100:            
            if dc_idx == SVC:   
                self.prog_timer[SVC].stop()
                self.progressBar_svc.setValue(100)
            else:
                self.prog_timer[H_K].stop()
                self.progressBar_obs.setValue(100)
                #self.elapsed_obs_timer.stop()
            return
        
        #print(dc_idx, "show_progressbar")
        self.cur_prog_step[dc_idx] += 1
        if dc_idx == SVC:
            self.progressBar_svc.setValue(self.cur_prog_step[dc_idx])
        else:
            self.progressBar_obs.setValue(self.cur_prog_step[dc_idx])

    
    # for HK
    def show_elapsed(self):
        cur_elapsed = self.elapsed_obs - (ti.time() - self.measure_T)
        if cur_elapsed <= 0 or self.cur_prog_step[H_K] >= 100:
            self.elapsed_obs_timer.stop()
            self.label_time_left.setText("0.000 sec")
            #self.prog_timer[H_K].stop()
            #self.progressBar_obs.setValue(100)
            return
        
        #print("show_elapsed")
        #self.elapsed_obs -= 0.001
        
        msg = "%.3f sec" % cur_elapsed
        self.label_time_left.setText(msg)
        
        
    def enable_dcss(self, enable):
        self.e_svc_fowler_number.setEnabled(enable)
        self.e_svc_exp_time.setEnabled(enable)
        
        self.chk_auto_save.setEnabled(enable)
        if enable:
            if self.chk_auto_save.isChecked():
                self.e_saving_number.setEnabled(True)
            else:
                self.e_repeat_file_name.setEnabled(True)
                self.bt_repeat_filesave.setEnabled(True)
        else:
            self.e_repeat_file_name.setEnabled(False)
            self.bt_repeat_filesave.setEnabled(False)
            self.e_saving_number.setEnabled(False)
        
        self.bt_center.setEnabled(enable)
                
        self.chk_off_slit.setEnabled(enable)
        if enable:
            if self.chk_off_slit.isChecked():
                self.bt_set_guide_star.setEnabled(True)
        else:
            self.bt_set_guide_star.setEnabled(False)        
    
        self.bt_plus_p.setEnabled(enable)
        self.bt_plus_q.setEnabled(enable)
        self.bt_minus_p.setEnabled(enable)
        self.bt_minus_q.setEnabled(enable)
        self.e_offset.setEnabled(enable)
        
        self.e_averaging_number.setEnabled(enable)
        

    
    #--------------------------------------------------------------
    # thread - with GUI
    # InstSeq -> DCS (ObsApp hooking)
    def InstSeq_data_processing(self):        
        if self.param_InstSeq == None:
            return
        
        param = self.param_InstSeq.split()
        print(param)
            
        # PA
        if param[0] == INSTSEQ_TCS_INFO_PA:
            self.label_IPA.setText(param[1])        
            self.PA = int(param[1])
            # current frame - A or B, A and B coordination
            
        elif param[0] == INSTSEQ_PQ:
            offset_p = int(param[1])
            offset_q = int(param[2])
            if (offset_p == 0 and offset_q > 0) or (offset_p == 0 and offset_q == 0):    
                self.cur_frame = A_BOX
            elif offset_p == 0 and offset_q < 0:  
                self.cur_frame = B_BOX
            elif offset_p != 0 and offset_q != 0: 
                self.cur_frame = OFF_BOX
            print(self.cur_frame)
                            
        elif param[0] == CMD_SETFSPARAM_ICS:       
            #self.stop_clicked = True            
            if param[1] == "all":
                if self.acquiring[SVC]:
                    self.abort_acquisition()
                    #self.bt_single.click()
                
                _fowlerTime = 1.63 - T_frame * 1
                _waittime = T_br + (T_frame + _fowlerTime + (2 * T_frame * 1))
                if self.cal_waittime[SVC] == 0:
                    self.cal_waittime[SVC] = _waittime
                    #print("cal_waittime SVC", self.cal_waittime[SVC])
                
                self.label_exp_time.setText(param[3])
                self.label_sampling_number.setText(param[4])
                _fowlerTime = float(param[5])
                self.cal_waittime[H_K] = T_br + (T_frame + _fowlerTime + (2 * T_frame * int(param[4])))
                #print("cal_waittime H_K", self.cal_waittime[H_K])
                
                self.elapsed_obs = self.cal_waittime[H_K]
                msg = "%.3f sec" % self.elapsed_obs
                self.label_time_left.setText(msg)    
                
            elif param[1] == "DCSS":
                if self.acquiring[SVC]:
                    self.abort_acquisition()
                    #self.bt_single.click()
                
                _fowlerTime = 1.63 - T_frame * 1
                _waittime = T_br + (T_frame + _fowlerTime + (2 * T_frame * 1))
                if self.cal_waittime[SVC] == 0:
                    self.cal_waittime[SVC] = _waittime
                    #print("cal_waittime SVC", self.cal_waittime[SVC])
            
            elif param[1] == "H_K":
                self.label_exp_time.setText(param[3])
                self.label_sampling_number.setText(param[4])
                _fowlerTime = float(param[5])
                self.cal_waittime[H_K] = T_br + (T_frame + _fowlerTime + (2 * T_frame * int(param[4])))
                #print("cal_waittime H_K", self.cal_waittime[H_K])
                
                self.elapsed_obs = self.cal_waittime[H_K]
                msg = "%.3f sec" % self.elapsed_obs
                self.label_time_left.setText(msg)
                
        elif param[0] == CMD_ACQUIRERAMP_ICS:
            #print("CMD_ACQUIRERAMP_ICS from InstSeq")  
            if param[1] == "all":
                self.label_svc_state.setText("Running")
                self.svc_progressbar_monit()
                
                self.label_obs_state.setText("Running")
                
                self.hk_progressbar_monit()

                self.acquiring[H] = True
                self.acquiring[K] = True

            elif param[1] == "DCSS":
                self.label_svc_state.setText("Running")
                self.svc_progressbar_monit()
                                            
            elif param[1] == "H_K":
                self.label_obs_state.setText("Running")
                self.hk_progressbar_monit()

                self.acquiring[H] = True
                self.acquiring[K] = True
                
        elif param[0] == CMD_STOPACQUISITION:
            if param[1] == "all":
                #self.cur_prog_step[SVC] = 100
                
                #self.cur_prog_step[H_K] = 100
                self.prog_timer[SVC].stop()
                
                self.prog_timer[H_K].stop()
                self.elapsed_obs_timer.stop()
                
                self.acquiring[H] = False
                self.acquiring[K] = False
                
            elif param[1] == "SVC":
                #self.cur_prog_step[SVC] = 100  
                self.prog_timer[SVC].stop() 
                                
            elif param[1] == "H_K":
                #self.cur_prog_step[H_K] = 100
                self.prog_timer[H_K].stop()
                self.elapsed_obs_timer.stop()
                
                self.acquiring[H] = False
                self.acquiring[K] = False
                
        self.param_InstSeq = None
                                        
                        
    def sub_data_processing(self):   
        # show value and color                    
        self.QShowValue(self.label_temp_detS, self.label_list[TMC2_A])
        self.QShowValue(self.label_temp_detK, self.label_list[TMC2_B])
        self.label_heater_detS.setText(self.heatlabel[self.label_list[TMC2_A]])
        self.label_heater_detK.setText(self.heatlabel[self.label_list[TMC2_B]])
        
        self.QShowValue(self.label_temp_detH, self.label_list[TMC3_B])
        self.label_heater_detH.setText(self.heatlabel[self.label_list[TMC3_B]])
                        
        # from VM
        self.label_vacuum.setText(self.dpvalue)
        
        # from Uploader
        if self.ig2_health == GOOD:
            self.label_is_health.setText("Good")
            self.QWidgetLabelColor(self.label_is_health, "green")
        elif self.ig2_health == WARNING:
            self.label_is_health.setText("Warning")
            self.QWidgetLabelColor(self.label_is_health, "gold")
        elif self.ig2_health == BAD:
            self.label_is_health.setText("Bad")
            self.QWidgetLabelColor(self.label_is_health, "red")
            
        
            
    # DCS -> InstSeq (ObsApp hooking)
    def dcs_data_processing_SVC(self):   
        if self.param_dcs[SVC] == None:
            return
            
        param = self.param_dcs[SVC].split()
        self.param_dcs[SVC] = None
                        
        try:
            if param[0] == CMD_INITIALIZE1:
                if int(param[2]) == 0:
                    self.dcss_ready = False
                    self.bt_single.setEnabled(False)
                    self.bt_slow_guide.setEnabled(False)
                    self.QWidgetBtnColor(self.bt_single, "silver")
                else:
                    self.dcss_ready = True
                    self.bt_single.setEnabled(True)
                    self.bt_slow_guide.setEnabled(True)
                    self.QWidgetBtnColor(self.bt_single, "black")
                    
            elif param[0] == CMD_INIT2_DONE or param[0] == CMD_INITIALIZE2_ICS:
                self.dcss_ready = True
                self.bt_single.setEnabled(True)
                self.bt_slow_guide.setEnabled(True)
                self.QWidgetBtnColor(self.bt_single, "black")

            elif param[0] == CMD_SETFSPARAM_ICS: 
                if not self.acquiring[SVC]:
                    return
                
                if not self.dcss_setparam:  
                    return
                    
                self.dcss_setparam = False
                msg = "%s DCSS %d 0" % (CMD_ACQUIRERAMP_ICS, self.simulation)
                self.publish_to_queue(msg)
            
            elif param[0] == CMD_ACQUIRERAMP_ICS:                     
                if len(param) == 1: 
                    return
                
                self.file_name = param[2]
                
                me = True
                if not self.acquiring[SVC]:
                    me = False
                self.acquiring[SVC] = False
                
                self.NFS_load_time = ti.time()
                        
                #self.prog_timer[SVC].stop()
                self.cur_prog_step[SVC] = 100
                #self.progressBar_svc.setValue(self.cur_prog_step[SVC])
                #("SVC progressbar: stop from SVC")
                
                self.label_svc_state.setText("Done")
                self.label_svc_filename.setText(param[2].split('/')[1]) 
                
                self.load_data(param[2])
                
                if self.svc_mode == SINGLE_MODE:
                    self.QWidgetBtnColor(self.bt_single, "black")
                    self.bt_single.setText("Exposure")
                    self.enable_dcss(True)
                    
                    self.bt_single.setEnabled(True)                        
                    self.bt_slow_guide.setEnabled(True)
                    
                    self.QWidgetBtnColor(self.bt_single, "black")
                
                else:
                    
                    #calculate center
                    #------------------------------
                    #20231006
                    dx = self.cen_x - self.guide_x
                    dy = self.cen_y - self.guide_y
                    #------------------------------
                    dp, dq = self.calc_xy_to_pq(dx, dy)
                    #dra, ddec = self.calc_pq_to_radec(dp, dq)
                    self.center_ra.append(dp)
                    self.center_dec.append(dq)
                    
                    if self.svc_mode == GUIDE_MODE:
                        self.cur_guide_cnt += 1
                        self.label_cur_Idx.setText(str(self.cur_guide_cnt) + " /")
                        if self.cur_guide_cnt >= int(self.e_averaging_number.text()):
                            
                            cen_ra_mean = np.mean(self.center_ra)
                            cen_dec_mean = np.mean(self.center_dec)
                            #tmp, no show in plot!!!               
                            
                            # send to TCS (offset)
                            self.move_to_telescope(cen_ra_mean, cen_dec_mean, SLOWGUIDING_MODE)
                                                    
                            self.cur_guide_cnt = 0 
                            self.center_ra = []
                            self.center_dec = []
                    
                    #if self.cur_save_cnt == 0:
                    #    msg = "%s %s" % (OBSAPP_SAVE_SVC, param[2])
                    #    self.publish_to_queue(msg)
                    
                    self.cur_save_cnt += 1
                    
                    if self.cur_save_cnt >= self.out_of_number_svc:
                        if self.chk_auto_save.isChecked():
                            ori_file = param[2].split('/')
                            foldername = ti.strftime("%02Y%02m%02d/", ti.localtime())
                            self.createFolder(self.svc_path + foldername)
                            
                            path = self.svc_path + foldername
                            dir_names = []
                            for names in os.listdir(path):
                                if names.find(".fits") >= 0:
                                    dir_names.append(names)
                            if len(dir_names) > 0:
                                next_idx = len(dir_names) + 1
                            else:
                                next_idx = 1
            
                            tmp = ori_file[1].split('_')
                            newfile = "%s%sO_%s_%s_%d.fits" % (self.svc_path, foldername, tmp[0], tmp[1], next_idx)
                            copyfile(self.fitsfullpath, newfile)
                        
                        self.cur_save_cnt = 0                          
                        
                    if self.stop_clicked:
                        self.stop_clicked = False
                        
                        self.cur_save_cnt = 0
                        
                        if self.svc_mode == CONT_MODE:
                            self.QWidgetBtnColor(self.bt_single, "black")
                        elif self.svc_mode == GUIDE_MODE:
                            self.QWidgetBtnColor(self.bt_slow_guide, "black")
                        
                        self.set_continue_mode()
                        
                        self.enable_dcss(True)
                        
                        self.bt_single.setEnabled(True)
                        self.bt_slow_guide.setEnabled(True)
                        self.QWidgetBtnColor(self.bt_single, "black")
                        
                        return    
                     
                    if me:
                        self.set_fs_param()    
                                    
            elif param[0] == CMD_STOPACQUISITION:  
                self.prog_timer[SVC].stop()
                
                self.bt_single.setEnabled(True)
                self.bt_slow_guide.setEnabled(True)
                        
                self.label_svc_state.setText("Idle")
                self.QWidgetBtnColor(self.bt_single, "black")
                self.bt_single.setText("Exposure")
                self.enable_dcss(True)
                
                self.acquiring[SVC] = False
                        
        except ZeroDivisionError:
            print("ZeroDivisionError")
        except ValueError:
            print("ValueError")
        except Exception as e:
            import traceback, sys
            traceback.print_exc(file=sys.stdout)
            
                    
            
    def dcs_data_processing_HK(self, idx): 
        if self.param_dcs[idx] == None:
            return
            
        param = self.param_dcs[idx].split()
        self.param_dcs[idx] = None
        
        if param[0] == CMD_ACQUIRERAMP_ICS:
            self.acquiring[idx] = False
            if not self.acquiring[H] and not self.acquiring[K]:
                self.cur_prog_step[H_K] = 100
                #self.progressBar_obs.setValue(self.cur_prog_step[H_K])
                #print("H progressbar: stop")

                self.label_obs_state.setText("Done")
                
        elif param[0] == CMD_STOPACQUISITION:
            self.acquiring[idx] = False
            if not self.acquiring[H] and not self.acquiring[K]:
                self.label_obs_state.setText("Idle")
                
                self.prog_timer[H_K].stop()
                self.elapsed_obs_timer.stop()
                
                
                                         
                         
    #-----------------------------------------------------------------------------------
    # for SW offset frame
    def setup_sw_offset_window(self, frame):
        from slit_centroid import MplFrame
        pixel_scale = PIXELSCALE
        self._sw_offset_finder = MplFrame(frame, 1.5, 1.,
                                          pixel_scale=pixel_scale)
        #self._sw_offset_finder.pack(side="top")
        
        
    def update_sw_offset(self, imgdata, mask):

        #cur_pos = self.cur_frame
        #nodding_mode = self._nodding_mode

        #if cur_pos not in "AB" or (cur_pos == "B" and nodding_mode != 0):
        if self.cur_frame == None or self.svc_mode != GUIDE_MODE or self.chk_off_slit.isChecked():
            self._sw_offset_finder.reset_image()
            return

        target = self.cur_frame

        try:
            if target == "A":
                gx, gy = (float(self.A_x), float(self.A_y))
            elif target == "B":
                gx, gy = (float(self.B_x), float(self.B_y))
        except:
            import traceback
            traceback.print_exc()
            return

        # 1004.5, 1047.6
        # PA = float(self.rotator.get()) + ROT_OFFSET
        PA = SLIT_ANG

        sw_slit_star_stack = self.sw_slit_star_get_stack()

        to_keep = self.sw_slit_star_get_height()
        sw_slit, sw_star = self._sw_offset_finder.update_image(
            imgdata, mask>0, gx, gy, PA,
            sw_slit_star_stack=(sw_slit_star_stack, to_keep))
        
        self.label_sw_slit.setText("{:.2}".format(float(sw_slit)))
        self.label_sw_star.setText("{:.2}".format(float(sw_star)))
        self.label_sw_star_slit.setText("{:.2}".format(float(sw_star - sw_slit)))
        
        self.sw_slit_star_push_offset(sw_slit, sw_star)
        
    
    def sw_slit_star_init(self):
        self._sw_slit_star_stack = []
        
        
    def sw_slit_star_get_height(self):
        to_keep = int(min(max(5,
                              int(self.e_averaging_number.text())),
        10))
        return to_keep
    
    
    def sw_slit_star_gc(self):
        to_keep = self.sw_slit_star_get_height()

        self._sw_slit_star_stack = self._sw_slit_star_stack[:to_keep*2]
    
        
    def sw_slit_star_get_stack(self):
        return self._sw_slit_star_stack
    
    
    def sw_slit_star_push_offset(self, sw_slit, sw_star):
        # i = len(self._sw_slit_star_stack)
        self._sw_slit_star_stack.insert(0, ("offset",
                                            # i,
                                            sw_slit,
                                            sw_star))
        self.sw_slit_star_gc()


if __name__ == "__main__":
    
    app = QApplication()
    sys.argv.append("True")
    ObsApp = MainWindow(sys.argv[1])
    ObsApp.show()
    #ObsApp.connect_to_server_dcs_q()
        
    app.exec()
