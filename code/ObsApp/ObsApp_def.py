# -*- coding: utf-8 -*-

"""
Created on Feb 10, 2023

Modified on 

@author: hilee
"""

# -----------------------------------------------------------
# definition: constant

import os

dir = os.getcwd().split("/")
WORKING_DIR = "/" + dir[1] + "/" + dir[2] + "/"

MAIN = "MAIN"
HK = "HK"
SC = "SC"
DCS = "DCS"

SUB_CNT = 3

# LOG option
DEBUG = "DEBUG"
INFO = "INFO"
WARNING = "WARNING"
ERROR = "ERROR"

GROUPBOX_IS = 0
GROUPBOX_SO = 1
FRM_EXPAND = 2
FRM_FITTING = 3
FRM_PROFILE = 4
FRM_SVC = 5
GROUPBOX_SVC = 6
GROUPBOX_SCALE = 7
LABEL_MSG = 8

SEL_NONE = 9
SEL_LOGFILE = 10
SEL_LOGLIST = 11
LIST_LOG = 12

SVC_FRAME_X = 2048
SVC_FRAME_Y = 2048

SINGLE_MODE = 0
CONT_MODE = 1
GUIDE_MODE = 2

DC_CNT = 3
SVC = 0
H_K = 1
ALL = 2

H = 1
K = 2

IMG_SVC = 0
IMG_EXPAND = 1
IMG_FITTING = 2
IMG_PROFILE = 3

T_frame = 1.45479
T_br = 2

# components
TMC2 = 0
TMC3 = 1
VM = 2

DEFAULT_VALUE = "-999"

TMC2_A = 0
TMC2_B = 1
TMC3_B = 2

ZOOMW = 32

G_BOX_CLR = "pink"
A_BOX_CLR = "red"
B_BOX_CLR = "cyan"
BOX_CLR = "green"

HK_REQ_GETVALUE = "GetValue"  #temp_ctrl, tm, vm

INSTSEQ_SHOW_TCS_INFO = "ShowTCSInfo"
OBSAPP_CAL_OFFSET = "CalOffset"
OBSAPP_BUSY = "ObsAppBusy"

CMD_INIT2_DONE = "Initialize2_Done" # to DCS
CMD_INITIALIZE2_ICS = "Initialize2_ics"
CMD_SETFSPARAM_ICS = "SetFSParam_ics"
CMD_ACQUIRERAMP_ICS = "ACQUIRERAMP_ics"
CMD_STOPACQUISITION = "STOPACQUISITION"

#CMD_COMPLETED = "Completed"
EXIT = "Exit"