# -*- coding: utf-8 -*-

"""
Created on Oct 21, 2022

Modified on May 22, 2023

@author: hilee
"""

import subprocess
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

import numpy as np
from scipy.ndimage.interpolation import rotate
import astropy.io.fits as fits 
import Libs.zscale as zs

#import glob

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle

from shutil import copyfile

from distutils.util import strtobool

class MainWindow(Ui_Dialog, QMainWindow):
    
    def __init__(self, simul):  #simulation mode: True
        super().__init__()
                
        #self.setGeometry(QRect(0, 0, 1253, 598))
        
        self.init_widget_rect = []
        self.prev_widget_rect = []      
        
        self.iam = "ObsApp"
        self.simulation = strtobool(simul)
        
        self.setupUi(self)
        
        self.log = LOG(WORKING_DIR+self.iam)  
        self.editlist_loglist.appendPlainText(self.log.send(self.iam, INFO, "start"))
        
        self.setWindowTitle("ObsApp 2.0")     
        
        # canvas        
        self.image_ax = [None for _ in range(4)]
        self.image_canvas = [None for _ in range(4)]
        for i in range(4):
            _image_fig = Figure(figsize=(4, 4), dpi=100)
            self.image_ax[i] = _image_fig.add_subplot(111)
            _image_fig.subplots_adjust(left=0.01,right=0.99,bottom=0.01,top=0.99) 
            self.image_canvas[i] = FigureCanvas(_image_fig)
                       
        vbox_svc = QVBoxLayout(self.frame_svc)
        vbox_svc.addWidget(self.image_canvas[IMG_SVC])
        vbox_svc = QVBoxLayout(self.frame_expand)
        vbox_svc.addWidget(self.image_canvas[IMG_EXPAND])
        vbox_svc = QVBoxLayout(self.frame_fitting)
        vbox_svc.addWidget(self.image_canvas[IMG_FITTING])
        vbox_svc = QVBoxLayout(self.frame_profile)
        vbox_svc.addWidget(self.image_canvas[IMG_PROFILE])
        
        self.clean_ax(self.image_ax[IMG_SVC])
        self.clean_ax(self.image_ax[IMG_EXPAND])
        #self.clean_ax(self.image_ax[IMG_FITTING])
        #self.clean_ax(self.image_ax[IMG_PROFILE])
        
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
        
        self.slit_cen = cfg.get(SC, 'slit-cen').split(",")
        
        self.svc_path = cfg.get(DCS,'data-location')
        
        self.key_to_label = dict()
        self.dtvalue, self.heatlabel = dict(), dict()
        self.temp_lower_warning, self.temp_lower_normal = dict(), dict()
        self.temp_upper_normal, self.temp_upper_warning = dict(), dict()
        self.det_sts = dict()
        
        self.label_list = ["tmc2-a", "tmc2-b", "tmc3-b"]
        self.dpvalue = DEFAULT_VALUE
        
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
        
        self.param_InstSeq = ""
        self.param_dcs = ["" for _ in range(DC_CNT)]
        
        self.svc_x, self.svc_y = float(self.slit_cen[0]), float(self.slit_cen[1])
        self.guide_x, self.guide_y = self.svc_x, self.svc_y
        self.A_x, self.A_y = self.svc_x-45, self.svc_y
        self.B_x, self.B_y = self.svc_x+45, self.svc_y
        
        #self.setMouseTracking(True)
        #self.setCursor(QCursor(Qt.CrossCursor))
                
        #--------------------------------
        # 0 - SVC, 1 - H_K
        
        self.dcss_ready = False
        self.acquiring = [False for _ in range(DC_CNT)]
        
        self.cur_save_cnt = 5
        self.cur_cal_cnt = 5
        self.center_ra, self.center_dec = [], []
        
        self.NFS_load_time = 0
                
        self.svc_mode = SINGLE_MODE
        self.cal_waittime = [0, 0]
        self.stop_clicked = False   # for continuous mode
        
        self.svc_header = None
        self.svc_img = None
        self.fitsfullpath = ""
        
        self.resize_enable = True
                
        # progress bar     
        self.prog_timer = [None, None]
        self.cur_prog_step = [None, None]
        
        # elapsed
        self.elapsed_obs_timer = None
        self.elapsed_obs = None
        self.measure_T = 0
        
        # from InstSeq, Position angle
        self.PA = 0
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
        self.e_svc_fowler_number.setText("16")
        self.e_svc_exp_time.setText("1.63")
        
        self.bt_single.setText("Exposure")
        
        # temp
        fname = ti.strftime("SDCS_%02Y%02m%02d_", ti.localtime())
        self.e_repeat_file_name.setText(fname)
        self.e_saving_number.setText(str(self.cur_save_cnt))
        
        self.e_offset.setText("1")
        
        self.e_averaging_number.setText(str(self.cur_cal_cnt))
        
        self.radio_raw.setChecked(True)
        self.radio_zscale.setChecked(True)
        
        self.label_zscale.setText("---")
        self.e_mscale_min.setText("1000")
        self.e_mscale_max.setText("5000")   
        
        self.radio_none.setChecked(True)
                
        # connect to rabbitmq
        self.connect_to_server_ObsApp_ex()
        
        self.connect_to_server_InstSeq_q()  #InstSeq
        self.connect_to_server_sub_q()  #TC2, TC3, VM
        self.connect_to_server_dcs_q()  #DCSS, DCSH, DCSK
                        
        self.InstSeq_timer = QTimer(self)
        self.InstSeq_timer.setInterval(0.1)
        self.InstSeq_timer.timeout.connect(self.InstSeq_data_processing)
        self.InstSeq_timer.start()
        
        self.show_sub_timer = QTimer(self)
        self.show_sub_timer.setInterval(self.Period/2)
        self.show_sub_timer.timeout.connect(self.sub_data_processing)
        self.show_sub_timer.start()
        
        self.show_dcs_timer = QTimer(self)
        self.show_dcs_timer.setInterval(0.1)
        self.show_dcs_timer.timeout.connect(self.dcs_data_processing)     
        self.show_dcs_timer.start()        
        
        msg = "%s DCSS %d" % (CMD_INIT2_DONE, self.simulation)
        self.publish_to_queue(msg)
                           
        self.auto_save_image()         
        self.set_off_slit()
        
        self.select_log_none()
        
        
    def closeEvent(self, event: QCloseEvent) -> None:        
        
        self.InstSeq_timer.stop()
        self.show_sub_timer.stop()
        self.show_dcs_timer.stop()
        
        self.editlist_loglist.appendPlainText(self.log.send(self.iam, DEBUG, "Closing %s : " % sys.argv[0]))
        self.editlist_loglist.appendPlainText(self.log.send(self.iam, DEBUG, "This may take several seconds waiting for threads to close"))      
                
        for th in threading.enumerate():
            self.editlist_loglist.appendPlainText(self.log.send(self.iam, INFO, th.name + " exit."))
        
        self.publish_to_queue(EXIT)
        
        if self.producer != None:
            self.producer.__del__()
        
        '''    
        self.producer.channel.close()
        self.consumer_InstSeq.channel.close()
        for i in range(DC_CNT):
            self.consumer_dcs[i].channel.close()
            self.consumer_sub[i].channel.close()
        '''
                            
        self.editlist_loglist.appendPlainText(self.log.send(self.iam, DEBUG, "Closed!"))
        
        return super().closeEvent(event)
    
    
    def init_events(self):
        
        self.editlist_loglist.setMaximumBlockCount(100)
        self.init_widget_rect = [None for _ in range(13)]
                
        self.image_canvas[IMG_SVC].mpl_connect('button_press_event', self.image_leftclick)
        
        self.self.chk_continue.clicked.connect(self.set_continue_mode)
        self.bt_single.clicked.connect(self.single)
        
        self.chk_auto_save.clicked.connect(self.auto_save_image)
        self.bt_repeat_filesave.clicked.connect(self.manual_filesave)
        
        self.bt_center.clicked.connect(self.set_center)
        self.chk_off_slit.clicked.connect(self.set_off_slit)
        self.bt_set_guide_star.clicked.connect(self.set_guide_star)
        
        self.bt_plus_p.clicked.connect(lambda: self.move_p(True))
        self.bt_minus_p.clicked.connect(lambda: self.move_p(False))
        self.bt_plus_q.clicked.connect(lambda: self.move_p(True))
        self.bt_minus_q.clicked.connect(lambda: self.move_p(False))
        
        self.bt_slow_guide.clicked.connect(self.slow_guide)
        
        self.radio_none.clicked.connect(self.select_log_none)
        self.radio_show_logfile.clicked.connect(self.select_log_file)
        self.radio_show_loglist.clicked.connect(self.select_log_list)
        
        self.bt_single.setEnabled(False)
        self.bt_set_guide_star.setEnabled(False)
        
        
        
    #--------------------------------------------------------
    # ObsApp publisher
    def connect_to_server_ObsApp_ex(self):
        self.producer = MsgMiddleware(self.iam, self.ics_ip_addr, self.ics_id, self.ics_pwd, self.ObsApp_ex)      
        self.producer.connect_to_server()
        self.producer.define_producer()
    
    '''
    def publish_to_queue(self, cmd, param=""):
        if self.producer == None:
            return
        
        msg = "%s %s %d" % (cmd, "DCSS", self.simulation)
        if param != "":
            msg += " " + param
        self.producer.send_message(self.ObsApp_q, msg)
        
        msg = "%s -> [DCSS]" % msg
        self.editlist_loglist.appendPlainText(self.log.send(self.iam, INFO, msg)) 
    '''
    
    def publish_to_queue(self, msg):
        if self.producer == None:
            return
        
        self.producer.send_message(self.ObsApp_q, msg)
        msg = "%s ->" % msg
        self.editlist_loglist.appendPlainText(self.log.send(self.iam, INFO, msg))
    
    
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
        self.editlist_loglist.appendPlainText(self.log.send(self.iam, INFO, msg))
        self.param_InstSeq = cmd
        
        
    #--------------------------------------------------------
    # tmc2, tmc3, vm queue
    def connect_to_server_sub_q(self):
        sub_list = ["tmc2", "tmc3", "vm"]
        
        sub_ObsApp_ex = [sub_list[i]+'.ex' for i in range(SUB_CNT)]
        self.consumer_sub = [None for _ in range(SUB_CNT)]
        for idx in range(SUB_CNT):
            self.consumer_sub[idx] = MsgMiddleware(self.iam, self.ics_ip_addr, self.ics_id, self.ics_pwd, sub_ObsApp_ex[idx])              
            self.consumer_sub[idx].connect_to_server()
                     
        self.consumer_sub[TMC2].define_consumer(sub_list[TMC2]+'.q', self.callback_tmc2)
        self.consumer_sub[TMC3].define_consumer(sub_list[TMC3]+'.q', self.callback_tmc3)
        self.consumer_sub[VM].define_consumer(sub_list[VM]+'.q', self.callback_vm)
        
        for idx in range(SUB_CNT):
            th = threading.Thread(target=self.consumer_sub[idx].start_consumer)
            th.daemon = True
            th.start()
            
    
    def callback_tmc2(self, ch, method, properties, body):
        cmd = body.decode()
        msg = "<- [TC2] %s" % cmd
        self.editlist_loglist.appendPlainText(self.log.send(self.iam, INFO, msg))
        param = cmd.split()
                
        if param[0] == HK_REQ_GETVALUE:
            self.dtvalue[self.label_list[TMC2_A]] = self.judge_value(param[1])
            self.dtvalue[self.label_list[TMC2_B]] = self.judge_value(param[2])
            self.heatlabel[self.label_list[TMC2_A]] = self.judge_value(param[3])
            self.heatlabel[self.label_list[TMC2_B]] = self.judge_value(param[4])
            
    
    def callback_tmc3(self, ch, method, properties, body):
        cmd = body.decode()
        msg = "<- [TC3] %s" % cmd
        self.editlist_loglist.appendPlainText(self.log.send(self.iam, INFO, msg))
        param = cmd.split()
                
        if param[0] == HK_REQ_GETVALUE:
            self.dtvalue[self.label_list[TMC3_B]] = self.judge_value(param[2])
            self.heatlabel[self.label_list[TMC3_B]] = self.judge_value(param[3])
            
    
    def callback_vm(self, ch, method, properties, body):
        cmd = body.decode()
        msg = "<- [VM] %s" % cmd
        if len(cmd) < 80:
            self.editlist_loglist.appendPlainText(self.log.send(self.iam, INFO, msg))
        param = cmd.split()
                    
        if param[0] == HK_REQ_GETVALUE:
            if len(param[1]) > 10 or param[1] == DEFAULT_VALUE:
                self.dpvalue = DEFAULT_VALUE
            else:
                self.dpvalue = param[1]
                   
    
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
        self.editlist_loglist.appendPlainText(self.log.send(self.iam, INFO, msg))
        self.param_dcs[SVC] = cmd  
                
        
    def callback_h(self, ch, method, properties, body):
        cmd = body.decode()
        msg = "<- [H] %s" % cmd
        self.editlist_loglist.appendPlainText(self.log.send(self.iam, INFO, msg))
        self.param_dcs[H] = cmd  
        
        
    def callback_k(self, ch, method, properties, body):
        cmd = body.decode()
        msg = "<- [K] %s" % cmd
        self.editlist_loglist.appendPlainText(self.log.send(self.iam, INFO, msg))
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
    
    
    def set_fs_param(self, first=False):     
        if not self.dcss_ready:
            return

        self.enable_dcss(False)  

        #setparam
        _exptime = float(self.e_svc_exp_time.text())
        _FS_number = int(self.e_svc_fowler_number.text())
        _fowlerTime = _exptime - T_frame * _FS_number
        _cal_waittime = T_br + (T_frame + _fowlerTime + (2 * T_frame * _FS_number))
                    
        self.label_svc_state.setText("Running")

        # progress bar 
        self.prog_timer[SVC] = QTimer(self)
        self.prog_timer[SVC].setInterval(int(_cal_waittime*10))   
        self.prog_timer[SVC].timeout.connect(lambda: self.show_progressbar(SVC))    

        self.cur_prog_step[SVC] = 0
        self.progressBar_svc.setValue(self.cur_prog_step[SVC])    
        self.prog_timer[SVC].start()   
        
        if first:
            msg = "%s DCSS %d %.3f 1 %d 1 %.3f 1" % (CMD_SETFSPARAM_ICS, self.simulation, _exptime, _FS_number, _fowlerTime)
        else:
            msg = "%s DCSS %d" % (CMD_ACQUIRERAMP_ICS, self.simulation)
        self.publish_to_queue(msg)

        
    def abort_acquisition(self):
        if self.cur_prog_step[SVC] > 0:
            self.prog_timer[SVC].stop()
              
        msg = "%s DCSS %d" % (CMD_STOPACQUISITION, self.simulation)
        self.publish_to_queue(msg)  
    
    
    def load_data(self, folder_name):
        
        self.label_svc_state.setText("Transfer")
        
        try:
            if self.simulation:
                self.fitsfullpath = "%sObsApp/SDCS_demo.fits" % WORKING_DIR
            else:
                self.fitsfullpath = "%sObsApp/dcss/Fowler/%s" % (WORKING_DIR, folder_name)

            frm = fits.open(self.fitsfullpath)
            msg = "%.5f" % (ti.time() - self.NFS_load_time)
            self.editlist_loglist.appendPlainText(self.log.send(self.iam, INFO, msg))
            
            data = frm[0].data
            self.svc_header = frm[0].header
            _img = np.array(data, dtype = "f")
            
            #_img = np.flipud(np.array(data, dtype = "f"))
            self.svc_img = rotate(_img, -45, axes=(1,0), reshape=None)
            
            self.zmin, self.zmax = zs.zscale(self.svc_img)
            range = "%d ~ %d" % (self.zmin, self.zmax)
            
            self.label_zscale.setText(range)
        
            self.mmin, self.mmax = np.min(self.svc_img[SVC]), np.max(self.svc_img[SVC])
            self.e_mscale_min.setText("%.1f" % self.mmin)
            self.e_mscale_max.setText("%.1f" % self.mmax)
                
            #if self.chk_autosave.isChecked():
            #    self.save_fits(dc_idx)
            
            self.reload_img()
        
        except:
            self.svc_img = None
            self.editlist_loglist.appendPlainText(self.log.send(self.iam, WARNING, "No image"))    
            
            
    def reload_img(self):
        
        try:
            # main draw                            
            _min, _max = 0, 0
            if self.radio_zscale.isChecked():
                _min, _max = self.zmin, self.zmax
            elif self.radio_mscale.isChecked():
                _min, _max = self.mmin, self.mmax
            
            self.display_coordinate(self.image_ax[IMG_SVC],self.svc_img, _min, _max, self.PA)
            if self.chk_off_slit.isChecked():
                self.display_box(self.image_ax[IMG_SVC], self.guide_x, self.guide_y, G_BOX_CLR)
            
            self.display_box(self.image_ax[IMG_SVC], self.A_x, self.A_y, A_BOX_CLR)
            self.display_box(self.image_ax[IMG_SVC], self.B_x, self.B_y, B_BOX_CLR)
            
            #self.display_box(self.image_ax[IMG_EXPAND], self.A_x, self.A_y, A_BOX_CLR)
            #self.display_box(self.image_ax[IMG_EXPAND], self.B_x, self.B_y, A_BOX_CLR)
            
            self.image_canvas[IMG_SVC].draw()
            
            self.load_img_zoom()
            
            self.label_svc_state.setText("Idle")
                
        except:
            self.svc_img = None
            self.editlist_loglist.appendPlainText(self.log.send(self.iam, WARNING, "No image"))
        
        
    def display_coordinate(self, imageax, imgdata, vmin, vmax, pa_tel):

        imageax.imshow(imgdata, vmin=vmin, vmax=vmax, cmap='gray', origin='lower')
                            
        imageax.axis('off')
        
        imageax.set_xlim(0, SVC_FRAME_X)
        imageax.set_xlim(0, SVC_FRAME_Y)
        
        cx, cy = 300, SVC_FRAME_Y-300
        arrow_size = 100
        text_ratio = 2
        
        PA = pa_tel
        u, v = (arrow_size*np.sin(np.deg2rad(PA)), arrow_size*np.cos(np.deg2rad(PA)))
        imageax.arrow(cx, cy, u, v, color="white", width=2, head_width=20)
        imageax.text(cx+u*text_ratio-40, cy+v*text_ratio*0.8, "N", color="white", size=10)
        PA = PA - 90
        u, v = (arrow_size*np.sin(np.deg2rad(PA)), arrow_size*np.cos(np.deg2rad(PA)))
        imageax.arrow(cx, cy, u, v, color="white", width=2, head_width=20)
        imageax.text(cx+u*text_ratio-10, cy+v*text_ratio-30, "E", color="white", size=10)
        
        cx = SVC_FRAME_X-150
        PA = 0
        u, v = (arrow_size*np.sin(np.deg2rad(PA)), arrow_size*np.cos(np.deg2rad(PA)))
        imageax.arrow(cx, cy, u, v, color="white", width=2, head_width=20)
        imageax.text(cx+u*text_ratio-60, cy+v*text_ratio*0.8, "+p", color="white", size=10)
        PA = PA - 90
        u, v = (arrow_size*np.sin(np.deg2rad(PA)), arrow_size*np.cos(np.deg2rad(PA)))
        imageax.arrow(cx, cy, u, v, color="white", width=2, head_width=20)
        imageax.text(cx+u*text_ratio*1.5, cy+v*text_ratio-30, "+q", color="white", size=10)

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
        if not (np.isfinite(x) and np.isfinite(x)):
            msg = "Invalid Value indisplay specialbox:", x, y
            self.logger.error(msg)
            return

        if (int(x) == 0 and int(y) == 0):
            return

        x_pos, y_pos = (int(x), int(y))

        zbox = Rectangle( (x_pos-ZOOMW, y_pos-ZOOMW), 2*ZOOMW+1, 2*ZOOMW+1, facecolor='none', edgecolor=boxcolor)
        ax.add_patch(zbox)

        ax.plot([x_pos-ZOOMW,x_pos+ZOOMW], [y_pos, y_pos], color=boxcolor)
        ax.plot([x_pos, x_pos], [y_pos-ZOOMW,y_pos+ZOOMW], color=boxcolor)
        
        
    def display_click(self, x_pos, y_pos):
        
        if (x_pos < 0) | (y_pos < 0): 
            return False
        if self.svc_img is None: 
            return False
        # make croped data
        ny, nx = self.svc_img.shape

        x_pos, y_pos = int(x_pos), int(y_pos)

        y1 = np.max([0, y_pos - ZOOMW])
        y2 = np.min([ny, y_pos + ZOOMW])
        x1 = np.max([0, x_pos - ZOOMW])
        x2 = np.min([nx, x_pos + ZOOMW])
        
        self.cropdata = self.svc_img[y1:y2, x1:x2]

        #add for test
        #self.cropdata = ndimage.rotate(self.cropdata, 45)
        self.cropmask = self.mask[y1:y2, x1:x2]

        '''
        # display pixel value and define click point in the crop image coordinate
        try:
            self.height, self.sx, self.sy, self.sigma, self.background = self.FindingCentroid(self.cropdata, self.cropmask, FITTING_2D_MASK)
            self.height_iMM = self.height

            msg = "Gaussian param"
            self.logger.debug(msg, extra=dict(height= self.height,
                                              sx=self.sx,
                                              sy=self.sy,
                                              sigma=self.sigma,
                                              bg=self.background))

            self.scframe.StatusInsert("P:%.0f B:%.0f X:%.1f Y:%.1f \nFWHM:%.2f" % (self.height, self.background, self.sx, self.sy, self.sigma*2.35482) )

            if not (np.isfinite(self.sx) and np.isfinite(self.sy)):
                self.sx, self.sy = x_pos - x1, y_pos - y1

        except Exception as e:
            #x_source_crop, y_source_crop = (0,0)
            import traceback, sys
            traceback.print_exc(file=sys.stdout)

            self.sx, self.sy = x_pos - x1, y_pos - y1

        #x_source_crop, y_source_crop = (self.sx, self.sy)

        # change coordinate for the full image
        source_x = self.sx + x1 # self.click_x - ZOOMW
        source_y = self.sy + y1 # self.click_y - ZOOMW

        self.draw_zoomin(self.cropdata, self.cropmask, source_x, source_y, self.sx, self.sy)

        # save the source position
        self.source_x, self.source_y = (source_x, source_y)

        self.show_GaussianFitting()

        return True
        '''
        
    def load_img_zoom(self):
        
        self.clean_ax(self.image_ax[IMG_EXPAND])
        
        try:                                
            # zoomin draw
            _x = self.svc_x
            _y = self.svc_y
            zoom_w = 100
            
            y1 = int(np.max([0, _y - zoom_w]))
            y2 = int(np.min([SVC_FRAME_Y, _y + zoom_w]))
            x1 = int(np.max([0, _x - zoom_w]))
            x2 = int(np.min([SVC_FRAME_X, _x + zoom_w]))
            
            _img_zoomin = self.svc_img[y1:y2, x1:x2]
            
            if self.radio_zscale.isChecked():
                _min, _max = self.zmin, self.zmax
            elif self.radio_mscale.isChecked():
                _min, _max = self.mmin, self.mmax
                
            self.image_ax[IMG_EXPAND].axis('off')
            self.image_ax[IMG_EXPAND].imshow(_img_zoomin, vmin=_min, vmax=_max, cmap='gray', origin='lower')
            self.image_canvas[IMG_EXPAND].draw()
            
            self.label_svc_state.setText("Idle")
                
        except:
            self.svc_img = None
            self.editlist_loglist.appendPlainText(self.log.send(self.iam, WARNING, "No image"))
    
    
    def clean_ax(self, ax, ticks_off = True):
        ax.cla()
        if (ticks_off == True):
            ax.set_xticklabels([])
            ax.set_yticklabels([])

            ax.set_frame_on(False)
            ax.set_xticks([])
            ax.set_yticks([])
            
    #--------------------------------------------------------
    # gui set
    def QShowValue(self, widget, label):
        value = self.dtvalue[label]
        name = "Det %s" % self.key_to_label[label][3:].upper()
        
        prev_sts = self.det_sts[label]
        
        if float(self.temp_lower_normal[label]) <= float(value) <= float(self.temp_upper_normal[label]):
            self.QWidgetLabelColor(widget, "green")
            msgbar = ""
            
            self.det_sts[label] = "good"
        
        else:
            color = ""
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
            self.editlist_loglist.appendPlainText(self.log.send(self.iam, INFO, msgbar))
        
    
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
        self.widget_resize(cur_width, cur_height, self.frame_profile, FRM_PROFILE)
        self.widget_resize(cur_width, cur_height, self.frame_svc, FRM_SVC)
        
        self.widget_resize(cur_width, cur_height, self.groupBox_SlitViewCamera, GROUPBOX_SVC)
        self.widget_resize(cur_width, cur_height, self.groupBox_zscale, GROUPBOX_SCALE)
        
        self.widget_resize(cur_width, cur_height, self.label_messagebar, LABEL_MSG)
        
        self.widget_resize(cur_width, cur_height, self.radio_none, SEL_NONE)
        self.widget_resize(cur_width, cur_height, self.radio_show_logfile, SEL_LOGFILE)
        self.widget_resize(cur_width, cur_height, self.radio_show_loglist, SEL_LOGLIST)
        
        self.widget_resize(cur_width, cur_height, self.editlist_loglist, LIST_LOG)

        self.prev_rect = self.geometry()
        
        return super().resizeEvent(event)    
    
    
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        print("Move (frame):", event.x(), event.y())
                
        self.mouse_x, self.mouse_y = event.x(), event.y()  
        
        return super().mouseMoveEvent(event)
        
    '''
    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            print("Mouse (frame):", self.mouse_x, self.mouse_y)
            print("Press (frame):", event.x(), event.y())
            print("self.prev_widget_rect[FRM_SVC]: ", self.prev_widget_rect[FRM_SVC])
            pixel_x = self.prev_widget_rect[FRM_SVC].width() / SVC_FRAME_X
            pixel_y = self.prev_widget_rect[FRM_SVC].height() / SVC_FRAME_Y
            self.svc_x = abs(self.mouse_x - self.prev_widget_rect[FRM_SVC].left()) / pixel_x
            self.svc_y = abs(self.mouse_y - self.prev_widget_rect[FRM_SVC].bottom()) / pixel_y
            print("pixel scale:", pixel_x, pixel_y)
            print("Press (svc):", self.svc_x, self.svc_y)
            
            self.load_img_zoom()
        return super().mousePressEvent(event)
    '''
    
    
    def image_leftclick(self, event):
        if event.xdata == None or event.ydata == None:
            return
        
        print("Press (frame):", event.xdata, event.ydata)
        #print("self.prev_widget_rect[FRM_SVC]: ", self.prev_widget_rect[FRM_SVC])
        self.svc_x = event.xdata
        self.svc_y = event.ydata
        print("Press (svc):", self.svc_x, self.svc_y)
        
        #self.display_click(self.svc_x, self.svc_y)
        
        self.load_img_zoom()
        
    
    def set_continue_mode(self):
        if self.chk_continue.isChecked():
            self.svc_mode = CONT_MODE
            self.stop_clicked = False
        else:
            self.svc_mode = SINGLE_MODE
            self.stop_clicked = True
        

    def single(self):
        
        if self.svc_mode == GUIDE_MODE:
            return
        
        if self.bt_single.text() == "Exposure":
            if self.svc_mode == CONT_MODE:
                self.bt_single.setText("Stop")                
                self.stop_clicked = False
            else:
                self.bt_single.setText("Abort")
                
            self.QWidgetBtnColor(self.bt_single, "yellow", "blue")
            self.set_fs_param(True)
            
        else:       
            if self.svc_mode == CONT_MODE:     
                self.stop_clicked = True   
            else:
                self.abort_acquisition()       
            
            self.bt_single.setText("Exposure")  
    
    
    def auto_save_image(self):
        if self.chk_auto_save.isChecked():
            self.e_saving_number.setEnabled(True)
            self.e_repeat_file_name.setEnabled(False)
            self.bt_repeat_filesave.setEnabled(False)
        else:
            self.e_saving_number.setEnabled(False)
            self.e_repeat_file_name.setEnabled(True)
            self.bt_repeat_filesave.setEnabled(True)
        
        
    def manual_filesave(self):        
        if self.fitsfullpath == "":
            return
        
        self.createFolder(self.svc_path)
        newfile = self.svc_path + self.e_repeat_file_name.text()
        copyfile(self.fitsfullpath, newfile)
        
        self.fitsfullpath = ""
        

    
    def set_center(self):
        pass
    
    
    def set_off_slit(self):
        self.clean_ax(self.image_ax[IMG_SVC])
        self.bt_set_guide_star.setEnabled(self.chk_off_slit.isChecked())
        if self.chk_off_slit.isChecked():
            self.display_box(self.image_ax[IMG_SVC], self.guide_x, self.guide_y, G_BOX_CLR)            
        self.reload_img()
    
    
    def set_guide_star(self):
        pass
        
        
    def move_p(self, north): #+:True, -:Minus 
        pass
    
    
    def move_q(self, west): #+:True, -:Minus 
        pass
    
    
    def slow_guide(self):
        self.svc_mode = GUIDE_MODE
        
        if self.bt_slow_guide.text() == "Slow Guide":
            self.bt_slow_guide.setText("Slow Guide Stop")
            self.stop_clicked = False
            
            self.QWidgetBtnColor(self.bt_slow_guide, "yellow", "blue")
            self.set_fs_param(True)
        else:
            self.bt_slow_guide.setText("Slow Guide") 
            self.stop_clicked = True
    
    
    def select_log_none(self):
        self.resize_enable = False
        
        self.radio_none.setChecked(True)
        self.radio_show_logfile.setChecked(False)
        self.radio_show_loglist.setChecked(False)
        
        self.setGeometry(QRect(0, 0, 900, 598))
        self.reset_resize()
            
    
    def select_log_file(self):
        self.resize_enable = False
        
        self.radio_none.setChecked(False)
        self.radio_show_logfile.setChecked(True)
        self.radio_show_loglist.setChecked(False)
        
        self.setGeometry(QRect(0, 0, 900, 598))
        self.reset_resize()
    
        # show log file
        logpath = WORKING_DIR + self.iam + '/Log/' + ti.strftime("%Y%m%d", ti.localtime())+".log"
        subprocess.Popen(['xdg-open', logpath])
        
        
    def select_log_list(self):
        self.resize_enable = False
        
        self.radio_none.setChecked(False)
        self.radio_show_logfile.setChecked(False)
        self.radio_show_loglist.setChecked(True)
        
        # show listview
        self.setGeometry(QRect(0, 0, 1253, 598))     
        self.reset_resize()
        
        
    def reset_resize(self):
        self.min_rect = self.geometry()
        self.prev_rect = self.min_rect
        print(self.min_rect)
        
        self.init_widget_rect[GROUPBOX_IS] = self.groupBox_InstrumentStatus.geometry()      # GROUPBOX_IS       
        self.init_widget_rect[GROUPBOX_SO] = self.groupBox_ScienceObservation.geometry()    # GROUPBOX_SO
            
        self.init_widget_rect[FRM_EXPAND] = self.frame_expand.geometry()                    # FRM_EXPAND
        self.init_widget_rect[FRM_FITTING] = self.frame_fitting.geometry()                  # FRM_FITTING
        self.init_widget_rect[FRM_PROFILE] = self.frame_profile.geometry()                  # FRM_PROFILE
        self.init_widget_rect[FRM_SVC] = self.frame_svc.geometry()                          # FRM_SVC
            
        self.init_widget_rect[GROUPBOX_SVC] = self.groupBox_SlitViewCamera.geometry()       # GROUPBOX_SVC
        self.init_widget_rect[GROUPBOX_SCALE] = self.groupBox_zscale.geometry()             # GROUPBOX_SCALE
        self.init_widget_rect[LABEL_MSG] = self.label_messagebar.geometry()                 # LABEL_MSG
        
        self.init_widget_rect[SEL_NONE] = self.radio_none.geometry()                        # SEL_NONE
        self.init_widget_rect[SEL_LOGFILE] = self.radio_show_logfile.geometry()             # SEL_LOGFILE
        self.init_widget_rect[SEL_LOGLIST] = self.radio_show_loglist.geometry()             # SEL_LOGLIST
        self.init_widget_rect[LIST_LOG] = self.editlist_loglist.geometry()                  # LIST_LOG
        
        self.prev_widget_rect = self.init_widget_rect
        
        self.resize_enable = True
        
     
    
    def show_progressbar(self, dc_idx):
        if self.cur_prog_step[dc_idx] >= 100:
            self.prog_timer[dc_idx].stop()
            return
        
        self.cur_prog_step[dc_idx] += 1
        if dc_idx == SVC:
            self.progressBar_svc.setValue(self.cur_prog_step[dc_idx])
        else:
            self.progressBar_obs.setValue(self.cur_prog_step[dc_idx])

    
    # for HK
    def show_elapsed(self):
        if self.elapsed_obs <= 0:
            self.elapsed_obs_timer.stop()
            return
        
        self.elapsed_obs -= 0.001
        msg = "%.3f sec" % self.elapsed_obs
        self.label_time_left.setText(msg)
        
        
    def enable_dcss(self, enable):
        self.e_svc_fowler_number.setEnabled(enable)
        self.e_svc_exp_time.setEnabled(enable)
        #self.bt_single.setEnabled(enable)
        
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
        
        self.bt_slow_guide.setEnabled(enable)
        self.e_averaging_number.setEnabled(enable)
        

    
    #--------------------------------------------------------------
    # thread - with GUI
    # InstSeq -> DCS (ObsApp hooking)
    def InstSeq_data_processing(self):        
        if self.param_InstSeq == "":
            return
        
        param = self.param_InstSeq.split()
            
        # PA
        if param[0] == INSTSEQ_SHOW_TCS_INFO:
            self.label_IPA.setText(param[1])
                    
        elif param[0] == CMD_SETFSPARAM_ICS:            
            if param[1] == "SVC" or param[1] == "all":
                
                if self.acquiring[SVC]:
                    self.publish_to_queue(OBSAPP_BUSY)
                    # continuous, single, or guiding mode -> stop!!!
                    self.bt_single.click()
                    return
                    
                self.e_svc_exp_time.setText(param[3])
                self.e_svc_fowler_number.setText(param[5])
                _fowlerTime = float(param[7])
                self.cal_waittime[SVC] = T_br + (T_frame + _fowlerTime + (2 * T_frame * int(param[5])))
                
                self.acquiring[SVC] = True
            
            if param[1] == "H_K" or param[1] == "all":
                self.label_exp_time.setText(param[3])
                self.label_sampling_number.setText(param[5])
                _fowlerTime = float(param[7])
                self.cal_waittime[H_K] = T_br + (T_frame + _fowlerTime + (2 * T_frame * int(param[5])))
                
                self.acquiring[H] = True
                self.acquiring[K] = True
                
        elif param[0] == CMD_ACQUIRERAMP_ICS:            
            if param[1] == "SVC" or param[1] == "all":
                self.enable_dcss(False)
                self.label_svc_state.setText("Running")
                
                #SVC progressbar
                self.prog_timer[SVC] = QTimer(self)
                self.prog_timer[SVC].setInterval(int(self.cal_waittime[SVC]*10))   
                self.prog_timer[SVC].timeout.connect(lambda: self.show_progressbar(SVC)) 
                
                self.cur_prog_step[SVC] = 0
                self.progressBar_obs.setValue(self.cur_prog_step[SVC])    
                self.prog_timer[SVC].start()   
                
                self.acquiring[SVC] = True
                            
            if param[1] == "H_K" or param[1] == "all":
                self.label_obs_state.setText("Running")
                
                #H, K progressbar
                self.prog_timer[H_K] = QTimer(self)
                self.prog_timer[H_K].setInterval(int(self.cal_waittime[H_K]*10))   
                self.prog_timer[H_K].timeout.connect(lambda: self.show_progressbar(H_K)) 
                
                self.cur_prog_step[H_K] = 0
                self.progressBar_obs.setValue(self.cur_prog_step[H_K])    
                self.prog_timer[H_K].start() 
                
                # elapsed               
                self.elapsed_obs_timer = QTimer(self) 
                self.elapsed_obs_timer.setInterval(0.001)
                self.elapsed_obs_timer.timeout.connect(self.show_elapsed)

                self.elapsed_obs = self.cal_waittime[H_K]
                self.label_time_left.setText(self.elapsed_obs)    
                self.elapsed_obs_timer.start()
                
        
        elif param[0] == CMD_STOPACQUISITION:
            if param[1] == "SVC" or param[1] == "all":
                self.prog_timer[SVC].stop()     
                
            if param[1] == "H_K" or param[1] == "all":
                self.prog_timer[H_K].stop()
                
                self.acquiring[H] = True
                self.acquiring[K] = True
            
        self.param_InstSeq = "" 
                            
                        
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
        
            
    # DCS -> InstSeq (ObsApp hooking)
    def dcs_data_processing(self):   
        #------------------------------------
        # svc             
        if self.param_dcs[SVC] != "":
            param = self.param_dcs[SVC].split()
            
            if param[0] == CMD_INIT2_DONE or param[0] == CMD_INITIALIZE2_ICS:
                self.dcss_ready = True
                self.bt_single.setEnabled(True)

            elif param[0] == CMD_SETFSPARAM_ICS:                
                msg = "%s DCSS %d" % (CMD_ACQUIRERAMP_ICS, self.simulation)
                self.publish_to_queue(msg)
            
            elif param[0] == CMD_ACQUIRERAMP_ICS:        
                self.acquiring[SVC] = False
                
                self.NFS_load_time = ti.time()
                           
                self.prog_timer[SVC].stop()
                self.cur_prog_step[SVC] = 100
                self.progressBar_svc.setValue(self.cur_prog_step[SVC])
                
                self.label_svc_state.setText("Done")
                self.label_svc_filename.setText(param[2]) 
                
                self.load_data(param[2])
                
                #calculate center
                center = [0, 0]
                self.center_ra.append(center[0])
                self.center_dec.append(center[1])
                self.cur_cal_cnt += 1
            
                cen_ra_mean, cen_dec_mean = 0, 0
                if self.cur_cal_cnt >= int(self.e_averaging_number.text()):
                    cen_ra_mean = np.mean(self.center_ra)
                    cen_dec_mean = np.mean(self.center_dec)
                    #tmp, no show in plot!!!               
                    
                    self.cur_cal_cnt = 0         
                            
                if self.svc_mode == CONT_MODE or self.svc_mode == GUIDE_MODE:
                    self.cur_save_cnt += 1
                    if self.chk_auto_save.isChecked() and self.cur_save_cnt >= int(self.e_saving_number.text()):
                        ori_file = param[2].split('/')
                        fullpath = self.svc_path + ori_file[0] + '/'
                        self.createFolder(fullpath)
                        # if someone want to rename the svc file name, it can be changed...
                        # save fname
                        newfile = fullpath + ori_file[1]
                        copyfile(self.fitsfullpath, newfile)
                                        
                        self.cur_save_cnt = 0 ?????
                        
                    if self.svc_mode == GUIDE_MODE and self.cur_cal_cnt == 0:
                        # send to TCS (offset)
                        msg = "%s %.3f %.3f" % (OBSAPP_CAL_OFFSET, cen_ra_mean, cen_dec_mean)
                        self.publish_to_queue(msg)   
                        
                    if self.stop_clicked:
                        self.stop_clicked = False
                        
                        self.cur_save_cnt = 0
                        
                        self.QWidgetBtnColor(self.bt_single, "black")
                        self.bt_single.setText("Exposure")
                        self.enable_dcss(True)
                        
                        self.param_dcs[SVC] = ""
                        return      
                                     
                    self.set_fs_param()                
                        
                else:
                    self.QWidgetBtnColor(self.bt_single, "black")
                    self.bt_single.setText("Exposure")
                    self.enable_dcss(True)
                    
            elif param[0] == CMD_STOPACQUISITION:   # for single mode                
                self.label_svc_state.setText("Idle")
                self.QWidgetBtnColor(self.bt_single, "black")
                self.bt_single.setText("Exposure")
                self.enable_dcss(True)
                
            self.param_dcs[SVC] = ""
        
        #------------------------------------
        # H    
        if self.param_dcs[H] != "":
            param = self.param_dcs[H].split()
            
            if param[0] == CMD_ACQUIRERAMP_ICS:
                self.acquiring[H] = False
                if not self.acquiring[H] and not self.acquiring[K]:
                    self.prog_timer[H_K].stop()
                    self.elapsed_obs_timer.stop()
                    
                    self.cur_prog_step[H_K] = 100
                    self.progressBar_obs.setValue(self.cur_prog_step[H_K])

                    self.label_obs_state.setText("Done")
                    
            elif param[0] == CMD_STOPACQUISITION:
                self.acquiring[H] = False
                if not self.acquiring[H] and not self.acquiring[K]:
                    self.label_obs_state.setText("Idle")
                    
            self.param_dcs[H] = ""
            
        #------------------------------------
        # K    
        if self.param_dcs[K] != "":
            param = self.param_dcs[K].split()
            
            if param[0] == CMD_ACQUIRERAMP_ICS:
                self.acquiring[K] = False
                if not self.acquiring[H] and not self.acquiring[K]:
                    self.prog_timer[H_K].stop()
                    self.elapsed_obs_timer.stop()
                    
                    self.cur_prog_step[H_K] = 100
                    self.progressBar_obs.setValue(self.cur_prog_step[H_K])

                    self.label_obs_state.setText("Done")
                    
            elif param[0] == CMD_STOPACQUISITION:
                self.acquiring[K] = False
                if not self.acquiring[H] and not self.acquiring[K]:
                    self.label_obs_state.setText("Idle")
                    
            self.param_dcs[K] = ""
            


if __name__ == "__main__":
    
    app = QApplication()
    sys.argv.append("True")
    ObsApp = MainWindow(sys.argv[1])
    ObsApp.show()
        
    app.exec()