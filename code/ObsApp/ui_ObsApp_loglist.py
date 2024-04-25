# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ObsApp_loglistFDTKqy.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QDialog, QListWidget,
    QListWidgetItem, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        #Dialog.setWindowModality(Qt.ApplicationModal)
        Dialog.resize(322, 661)
        #Dialog.setModal(False)
        self.listWidget_log = QListWidget(Dialog)
        self.listWidget_log.setObjectName(u"listWidget_log")
        self.listWidget_log.setGeometry(QRect(10, 10, 301, 641))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget_log.sizePolicy().hasHeightForWidth())
        self.listWidget_log.setSizePolicy(sizePolicy)
        self.listWidget_log.setMaximumSize(QSize(16777211, 16777215))
        self.listWidget_log.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.listWidget_log.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
    # retranslateUi

