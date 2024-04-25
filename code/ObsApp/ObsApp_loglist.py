# -*- coding: utf-8 -*-

"""
Created on Apr 24, 2024

Modified on

@author: hilee
"""

from ObsApp_def import *
from ui_ObsApp_loglist import *

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class LogListDlg(Ui_Dialog, QMainWindow):
    
    def __init__(self):
        super().__init__()  
        
        self.setFixedSize(322, 661)
        
        self.setupUi(self)
        
        self.setWindowTitle("Log List")  
            
        
    def dlg_init(self, x_pos, y_pos):
        self.setGeometry(x_pos, y_pos, 322, 661)
        
    
    def show_log(self, log_option, msg):
        if self.listWidget_log.count() >= 70:
            self.listWidget_log.takeItem(0)
        self.listWidget_log.addItem(msg)
            
        if self.listWidget_log.count() != 0:
            if log_option == WARNING:
                self.listWidget_log.item(self.listWidget_log.count()-1).setForeground(QColor("gold"))
            elif log_option == ERROR:
                self.listWidget_log.item(self.listWidget_log.count()-1).setForeground(QColor("red"))
            else:
                if msg.find(OBSAPP_CAL_OFFSET) >= 0:
                    self.listWidget_log.item(self.listWidget_log.count()-1).setForeground(QColor("green"))
                else:
                    self.listWidget_log.item(self.listWidget_log.count()-1).setForeground(QColor("black"))

    
