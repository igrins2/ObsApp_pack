# -*- coding: utf-8 -*-

################################################################################
<<<<<<< Updated upstream
## Form generated from reading UI file 'ObsAppnMaUCC.ui'
=======
## Form generated from reading UI file 'ObsAppeMjoQS.ui'
>>>>>>> Stashed changes
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QFrame, QGridLayout, QGroupBox, QLabel,
    QLineEdit, QProgressBar, QPushButton, QRadioButton,
    QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(892, 733)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setAutoFillBackground(False)
        #Dialog.setSizeGripEnabled(False)
        #Dialog.setModal(False)
        self.groupBox_InstrumentStatus = QGroupBox(Dialog)
        self.groupBox_InstrumentStatus.setObjectName(u"groupBox_InstrumentStatus")
<<<<<<< Updated upstream
        self.groupBox_InstrumentStatus.setGeometry(QRect(10, 10, 221, 378))
=======
        self.groupBox_InstrumentStatus.setGeometry(QRect(10, 6, 221, 431))
>>>>>>> Stashed changes
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox_InstrumentStatus.sizePolicy().hasHeightForWidth())
        self.groupBox_InstrumentStatus.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setPointSize(8)
        self.groupBox_InstrumentStatus.setFont(font)
        self.gridLayout_7 = QGridLayout(self.groupBox_InstrumentStatus)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.label_g1 = QLabel(self.groupBox_InstrumentStatus)
        self.label_g1.setObjectName(u"label_g1")
        sizePolicy.setHeightForWidth(self.label_g1.sizePolicy().hasHeightForWidth())
        self.label_g1.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setPointSize(13)
        font1.setBold(True)
        self.label_g1.setFont(font1)
        self.label_g1.setAlignment(Qt.AlignCenter)

<<<<<<< Updated upstream
        self.gridLayout.addWidget(self.label_g1, 0, 0, 1, 3)
=======
        self.gridLayout_7.addWidget(self.label_g1, 0, 0, 1, 4)
>>>>>>> Stashed changes

        self.label_heartbeat = QLabel(self.groupBox_InstrumentStatus)
        self.label_heartbeat.setObjectName(u"label_heartbeat")
        font2 = QFont()
        font2.setPointSize(12)
        self.label_heartbeat.setFont(font2)
        self.label_heartbeat.setAlignment(Qt.AlignCenter)

<<<<<<< Updated upstream
        self.gridLayout.addWidget(self.label_heartbeat, 1, 0, 1, 1)
=======
        self.gridLayout_7.addWidget(self.label_heartbeat, 1, 0, 1, 2)
>>>>>>> Stashed changes

        self.label_g1_1 = QLabel(self.groupBox_InstrumentStatus)
        self.label_g1_1.setObjectName(u"label_g1_1")
        sizePolicy.setHeightForWidth(self.label_g1_1.sizePolicy().hasHeightForWidth())
        self.label_g1_1.setSizePolicy(sizePolicy)
        font3 = QFont()
        font3.setPointSize(12)
        font3.setBold(True)
        self.label_g1_1.setFont(font3)
<<<<<<< Updated upstream
        self.label_g1_1.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_g1_1, 1, 1, 1, 1)

        self.label_is_health = QLabel(self.groupBox_InstrumentStatus)
        self.label_is_health.setObjectName(u"label_is_health")
        sizePolicy.setHeightForWidth(self.label_is_health.sizePolicy().hasHeightForWidth())
        self.label_is_health.setSizePolicy(sizePolicy)
        font4 = QFont()
        font4.setPointSize(10)
        font4.setBold(True)
        self.label_is_health.setFont(font4)
        self.label_is_health.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_is_health, 1, 2, 1, 1)

        self.label_g1_13 = QLabel(self.groupBox_InstrumentStatus)
        self.label_g1_13.setObjectName(u"label_g1_13")
        font5 = QFont()
        font5.setPointSize(10)
        self.label_g1_13.setFont(font5)
        self.label_g1_13.setLayoutDirection(Qt.LeftToRight)
        self.label_g1_13.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_g1_13, 2, 1, 1, 1)

        self.label_ics_health = QLabel(self.groupBox_InstrumentStatus)
        self.label_ics_health.setObjectName(u"label_ics_health")
        self.label_ics_health.setFont(font4)

        self.gridLayout.addWidget(self.label_ics_health, 2, 2, 1, 1)
=======
        self.label_g1_1.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.label_g1_1, 1, 2, 1, 1)

        self.label_heartbeat_ics = QLabel(self.groupBox_InstrumentStatus)
        self.label_heartbeat_ics.setObjectName(u"label_heartbeat_ics")
        font4 = QFont()
        font4.setPointSize(12)
        self.label_heartbeat_ics.setFont(font4)
        self.label_heartbeat_ics.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.label_heartbeat_ics, 2, 0, 1, 1)

        self.label_g1_13 = QLabel(self.groupBox_InstrumentStatus)
        self.label_g1_13.setObjectName(u"label_g1_13")
        font5 = QFont()
        font5.setPointSize(10)
        self.label_g1_13.setFont(font5)
        self.label_g1_13.setLayoutDirection(Qt.LeftToRight)
        self.label_g1_13.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_g1_13, 2, 1, 1, 2)

        self.label_state_ics = QLabel(self.groupBox_InstrumentStatus)
        self.label_state_ics.setObjectName(u"label_state_ics")
        sizePolicy.setHeightForWidth(self.label_state_ics.sizePolicy().hasHeightForWidth())
        self.label_state_ics.setSizePolicy(sizePolicy)
        font6 = QFont()
        font6.setPointSize(9)
        font6.setBold(True)
        self.label_state_ics.setFont(font6)
        self.label_state_ics.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_state_ics, 2, 3, 1, 1)

        self.label_heartbeat_dcsh = QLabel(self.groupBox_InstrumentStatus)
        self.label_heartbeat_dcsh.setObjectName(u"label_heartbeat_dcsh")
        self.label_heartbeat_dcsh.setFont(font4)
        self.label_heartbeat_dcsh.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.label_heartbeat_dcsh, 3, 0, 1, 1)
>>>>>>> Stashed changes

        self.label_g1_14 = QLabel(self.groupBox_InstrumentStatus)
        self.label_g1_14.setObjectName(u"label_g1_14")
        self.label_g1_14.setFont(font5)
        self.label_g1_14.setLayoutDirection(Qt.LeftToRight)
<<<<<<< Updated upstream
        self.label_g1_14.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_g1_14, 3, 0, 1, 2)

        self.label_dcsh_health = QLabel(self.groupBox_InstrumentStatus)
        self.label_dcsh_health.setObjectName(u"label_dcsh_health")
        self.label_dcsh_health.setFont(font4)

        self.gridLayout.addWidget(self.label_dcsh_health, 3, 2, 1, 1)
=======
        self.label_g1_14.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_g1_14, 3, 1, 1, 2)

        self.label_state_dcsh = QLabel(self.groupBox_InstrumentStatus)
        self.label_state_dcsh.setObjectName(u"label_state_dcsh")
        sizePolicy.setHeightForWidth(self.label_state_dcsh.sizePolicy().hasHeightForWidth())
        self.label_state_dcsh.setSizePolicy(sizePolicy)
        self.label_state_dcsh.setFont(font6)
        self.label_state_dcsh.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_state_dcsh, 3, 3, 1, 1)

        self.label_heartbeat_dcsk = QLabel(self.groupBox_InstrumentStatus)
        self.label_heartbeat_dcsk.setObjectName(u"label_heartbeat_dcsk")
        self.label_heartbeat_dcsk.setFont(font4)
        self.label_heartbeat_dcsk.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.label_heartbeat_dcsk, 4, 0, 1, 1)
>>>>>>> Stashed changes

        self.label_g1_15 = QLabel(self.groupBox_InstrumentStatus)
        self.label_g1_15.setObjectName(u"label_g1_15")
        self.label_g1_15.setFont(font5)
        self.label_g1_15.setLayoutDirection(Qt.LeftToRight)
<<<<<<< Updated upstream
        self.label_g1_15.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_g1_15, 4, 0, 1, 2)

        self.label_dcsk_health = QLabel(self.groupBox_InstrumentStatus)
        self.label_dcsk_health.setObjectName(u"label_dcsk_health")
        self.label_dcsk_health.setFont(font4)

        self.gridLayout.addWidget(self.label_dcsk_health, 4, 2, 1, 1)
=======
        self.label_g1_15.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_g1_15, 4, 1, 1, 2)

        self.label_state_dcsk = QLabel(self.groupBox_InstrumentStatus)
        self.label_state_dcsk.setObjectName(u"label_state_dcsk")
        sizePolicy.setHeightForWidth(self.label_state_dcsk.sizePolicy().hasHeightForWidth())
        self.label_state_dcsk.setSizePolicy(sizePolicy)
        self.label_state_dcsk.setFont(font6)
        self.label_state_dcsk.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_state_dcsk, 4, 3, 1, 1)

        self.label_heartbeat_dcss = QLabel(self.groupBox_InstrumentStatus)
        self.label_heartbeat_dcss.setObjectName(u"label_heartbeat_dcss")
        self.label_heartbeat_dcss.setFont(font4)
        self.label_heartbeat_dcss.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.label_heartbeat_dcss, 5, 0, 1, 1)
>>>>>>> Stashed changes

        self.label_g1_24 = QLabel(self.groupBox_InstrumentStatus)
        self.label_g1_24.setObjectName(u"label_g1_24")
        self.label_g1_24.setFont(font5)
        self.label_g1_24.setLayoutDirection(Qt.LeftToRight)
        self.label_g1_24.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

<<<<<<< Updated upstream
        self.gridLayout.addWidget(self.label_g1_24, 5, 0, 1, 2)

        self.label_dcss_health = QLabel(self.groupBox_InstrumentStatus)
        self.label_dcss_health.setObjectName(u"label_dcss_health")
        self.label_dcss_health.setFont(font4)

        self.gridLayout.addWidget(self.label_dcss_health, 5, 2, 1, 1)

        self.label_g1_2 = QLabel(self.groupBox_InstrumentStatus)
        self.label_g1_2.setObjectName(u"label_g1_2")
        sizePolicy.setHeightForWidth(self.label_g1_2.sizePolicy().hasHeightForWidth())
        self.label_g1_2.setSizePolicy(sizePolicy)
        font6 = QFont()
        font6.setPointSize(10)
        font6.setBold(False)
        self.label_g1_2.setFont(font6)
        self.label_g1_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_g1_2, 6, 1, 1, 1)

        self.label_GDSN_connection = QLabel(self.groupBox_InstrumentStatus)
        self.label_GDSN_connection.setObjectName(u"label_GDSN_connection")
        sizePolicy.setHeightForWidth(self.label_GDSN_connection.sizePolicy().hasHeightForWidth())
        self.label_GDSN_connection.setSizePolicy(sizePolicy)
        self.label_GDSN_connection.setFont(font4)
        self.label_GDSN_connection.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_GDSN_connection, 6, 2, 1, 1)
=======
        self.gridLayout_7.addWidget(self.label_g1_24, 5, 1, 1, 2)

        self.label_state_dcss = QLabel(self.groupBox_InstrumentStatus)
        self.label_state_dcss.setObjectName(u"label_state_dcss")
        sizePolicy.setHeightForWidth(self.label_state_dcss.sizePolicy().hasHeightForWidth())
        self.label_state_dcss.setSizePolicy(sizePolicy)
        self.label_state_dcss.setFont(font6)
        self.label_state_dcss.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_state_dcss, 5, 3, 1, 1)

        self.label_heartbeat_InstSeq = QLabel(self.groupBox_InstrumentStatus)
        self.label_heartbeat_InstSeq.setObjectName(u"label_heartbeat_InstSeq")
        self.label_heartbeat_InstSeq.setFont(font4)
        self.label_heartbeat_InstSeq.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.label_heartbeat_InstSeq, 6, 0, 1, 1)

        self.label_InstSeq_connect = QLabel(self.groupBox_InstrumentStatus)
        self.label_InstSeq_connect.setObjectName(u"label_InstSeq_connect")
        sizePolicy.setHeightForWidth(self.label_InstSeq_connect.sizePolicy().hasHeightForWidth())
        self.label_InstSeq_connect.setSizePolicy(sizePolicy)
        font7 = QFont()
        font7.setPointSize(10)
        font7.setBold(False)
        self.label_InstSeq_connect.setFont(font7)
        self.label_InstSeq_connect.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_InstSeq_connect, 6, 1, 1, 2)

        self.label_state_InstSeq = QLabel(self.groupBox_InstrumentStatus)
        self.label_state_InstSeq.setObjectName(u"label_state_InstSeq")
        sizePolicy.setHeightForWidth(self.label_state_InstSeq.sizePolicy().hasHeightForWidth())
        self.label_state_InstSeq.setSizePolicy(sizePolicy)
        self.label_state_InstSeq.setFont(font6)
        self.label_state_InstSeq.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_state_InstSeq, 6, 3, 1, 1)

        self.label_heartbeat_dbuploader = QLabel(self.groupBox_InstrumentStatus)
        self.label_heartbeat_dbuploader.setObjectName(u"label_heartbeat_dbuploader")
        self.label_heartbeat_dbuploader.setFont(font4)
        self.label_heartbeat_dbuploader.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.label_heartbeat_dbuploader, 7, 0, 1, 1)

        self.label_db_uploader = QLabel(self.groupBox_InstrumentStatus)
        self.label_db_uploader.setObjectName(u"label_db_uploader")
        sizePolicy.setHeightForWidth(self.label_db_uploader.sizePolicy().hasHeightForWidth())
        self.label_db_uploader.setSizePolicy(sizePolicy)
        self.label_db_uploader.setFont(font7)
        self.label_db_uploader.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_db_uploader, 7, 1, 1, 2)

        self.label_state_dbuploader = QLabel(self.groupBox_InstrumentStatus)
        self.label_state_dbuploader.setObjectName(u"label_state_dbuploader")
        sizePolicy.setHeightForWidth(self.label_state_dbuploader.sizePolicy().hasHeightForWidth())
        self.label_state_dbuploader.setSizePolicy(sizePolicy)
        self.label_state_dbuploader.setFont(font6)
        self.label_state_dbuploader.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_state_dbuploader, 7, 3, 1, 1)

        self.label_heartbeat_gmp = QLabel(self.groupBox_InstrumentStatus)
        self.label_heartbeat_gmp.setObjectName(u"label_heartbeat_gmp")
        self.label_heartbeat_gmp.setFont(font4)
        self.label_heartbeat_gmp.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.label_heartbeat_gmp, 8, 0, 1, 1)
>>>>>>> Stashed changes

        self.label_g1_3 = QLabel(self.groupBox_InstrumentStatus)
        self.label_g1_3.setObjectName(u"label_g1_3")
        sizePolicy.setHeightForWidth(self.label_g1_3.sizePolicy().hasHeightForWidth())
        self.label_g1_3.setSizePolicy(sizePolicy)
<<<<<<< Updated upstream
        self.label_g1_3.setFont(font6)
        self.label_g1_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_g1_3, 7, 1, 1, 1)

        self.label_GMP_connection = QLabel(self.groupBox_InstrumentStatus)
        self.label_GMP_connection.setObjectName(u"label_GMP_connection")
        sizePolicy.setHeightForWidth(self.label_GMP_connection.sizePolicy().hasHeightForWidth())
        self.label_GMP_connection.setSizePolicy(sizePolicy)
        self.label_GMP_connection.setFont(font4)
        self.label_GMP_connection.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_GMP_connection, 7, 2, 1, 1)
=======
        self.label_g1_3.setFont(font7)
        self.label_g1_3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_g1_3, 8, 1, 1, 2)

        self.label_state_gmp = QLabel(self.groupBox_InstrumentStatus)
        self.label_state_gmp.setObjectName(u"label_state_gmp")
        sizePolicy.setHeightForWidth(self.label_state_gmp.sizePolicy().hasHeightForWidth())
        self.label_state_gmp.setSizePolicy(sizePolicy)
        self.label_state_gmp.setFont(font6)
        self.label_state_gmp.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_state_gmp, 8, 3, 1, 1)
>>>>>>> Stashed changes

        self.label_g1_4 = QLabel(self.groupBox_InstrumentStatus)
        self.label_g1_4.setObjectName(u"label_g1_4")
        sizePolicy.setHeightForWidth(self.label_g1_4.sizePolicy().hasHeightForWidth())
        self.label_g1_4.setSizePolicy(sizePolicy)
        self.label_g1_4.setFont(font7)
        self.label_g1_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

<<<<<<< Updated upstream
        self.gridLayout.addWidget(self.label_g1_4, 8, 1, 1, 1)
=======
        self.gridLayout_7.addWidget(self.label_g1_4, 9, 2, 1, 1)
>>>>>>> Stashed changes

        self.label_state = QLabel(self.groupBox_InstrumentStatus)
        self.label_state.setObjectName(u"label_state")
        sizePolicy.setHeightForWidth(self.label_state.sizePolicy().hasHeightForWidth())
        self.label_state.setSizePolicy(sizePolicy)
<<<<<<< Updated upstream
        self.label_state.setFont(font4)
        self.label_state.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_state, 8, 2, 1, 1)
=======
        font8 = QFont()
        font8.setPointSize(10)
        font8.setBold(True)
        self.label_state.setFont(font8)
        self.label_state.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_state, 9, 3, 1, 1)
>>>>>>> Stashed changes

        self.label_g1_5 = QLabel(self.groupBox_InstrumentStatus)
        self.label_g1_5.setObjectName(u"label_g1_5")
        sizePolicy.setHeightForWidth(self.label_g1_5.sizePolicy().hasHeightForWidth())
        self.label_g1_5.setSizePolicy(sizePolicy)
        self.label_g1_5.setFont(font7)
        self.label_g1_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

<<<<<<< Updated upstream
        self.gridLayout.addWidget(self.label_g1_5, 9, 1, 1, 1)
=======
        self.gridLayout_7.addWidget(self.label_g1_5, 10, 0, 1, 3)
>>>>>>> Stashed changes

        self.label_action_state = QLabel(self.groupBox_InstrumentStatus)
        self.label_action_state.setObjectName(u"label_action_state")
        sizePolicy.setHeightForWidth(self.label_action_state.sizePolicy().hasHeightForWidth())
        self.label_action_state.setSizePolicy(sizePolicy)
<<<<<<< Updated upstream
        self.label_action_state.setFont(font4)
        self.label_action_state.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_action_state, 9, 2, 1, 1)
=======
        self.label_action_state.setFont(font8)
        self.label_action_state.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_action_state, 10, 3, 1, 1)
>>>>>>> Stashed changes

        self.label_g1_7 = QLabel(self.groupBox_InstrumentStatus)
        self.label_g1_7.setObjectName(u"label_g1_7")
        sizePolicy.setHeightForWidth(self.label_g1_7.sizePolicy().hasHeightForWidth())
        self.label_g1_7.setSizePolicy(sizePolicy)
        self.label_g1_7.setFont(font7)
        self.label_g1_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

<<<<<<< Updated upstream
        self.gridLayout.addWidget(self.label_g1_7, 10, 1, 1, 1)
=======
        self.gridLayout_7.addWidget(self.label_g1_7, 11, 1, 1, 2)
>>>>>>> Stashed changes

        self.label_temp_detH = QLabel(self.groupBox_InstrumentStatus)
        self.label_temp_detH.setObjectName(u"label_temp_detH")
        sizePolicy.setHeightForWidth(self.label_temp_detH.sizePolicy().hasHeightForWidth())
        self.label_temp_detH.setSizePolicy(sizePolicy)
<<<<<<< Updated upstream
        self.label_temp_detH.setFont(font4)
        self.label_temp_detH.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_temp_detH, 10, 2, 1, 1)
=======
        self.label_temp_detH.setFont(font8)
        self.label_temp_detH.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_temp_detH, 11, 3, 1, 1)
>>>>>>> Stashed changes

        self.label_g1_8 = QLabel(self.groupBox_InstrumentStatus)
        self.label_g1_8.setObjectName(u"label_g1_8")
        sizePolicy.setHeightForWidth(self.label_g1_8.sizePolicy().hasHeightForWidth())
        self.label_g1_8.setSizePolicy(sizePolicy)
        self.label_g1_8.setFont(font7)
        self.label_g1_8.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

<<<<<<< Updated upstream
        self.gridLayout.addWidget(self.label_g1_8, 11, 1, 1, 1)
=======
        self.gridLayout_7.addWidget(self.label_g1_8, 12, 1, 1, 2)
>>>>>>> Stashed changes

        self.label_temp_detK = QLabel(self.groupBox_InstrumentStatus)
        self.label_temp_detK.setObjectName(u"label_temp_detK")
        sizePolicy.setHeightForWidth(self.label_temp_detK.sizePolicy().hasHeightForWidth())
        self.label_temp_detK.setSizePolicy(sizePolicy)
<<<<<<< Updated upstream
        self.label_temp_detK.setFont(font4)
        self.label_temp_detK.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_temp_detK, 11, 2, 1, 1)
=======
        self.label_temp_detK.setFont(font8)
        self.label_temp_detK.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_temp_detK, 12, 3, 1, 1)
>>>>>>> Stashed changes

        self.label_g1_9 = QLabel(self.groupBox_InstrumentStatus)
        self.label_g1_9.setObjectName(u"label_g1_9")
        sizePolicy.setHeightForWidth(self.label_g1_9.sizePolicy().hasHeightForWidth())
        self.label_g1_9.setSizePolicy(sizePolicy)
        self.label_g1_9.setFont(font7)
        self.label_g1_9.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

<<<<<<< Updated upstream
        self.gridLayout.addWidget(self.label_g1_9, 12, 1, 1, 1)
=======
        self.gridLayout_7.addWidget(self.label_g1_9, 13, 1, 1, 2)
>>>>>>> Stashed changes

        self.label_temp_detS = QLabel(self.groupBox_InstrumentStatus)
        self.label_temp_detS.setObjectName(u"label_temp_detS")
        sizePolicy.setHeightForWidth(self.label_temp_detS.sizePolicy().hasHeightForWidth())
        self.label_temp_detS.setSizePolicy(sizePolicy)
<<<<<<< Updated upstream
        self.label_temp_detS.setFont(font4)
        self.label_temp_detS.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_temp_detS, 12, 2, 1, 1)

        self.groupBox_ScienceObservation = QGroupBox(Dialog)
        self.groupBox_ScienceObservation.setObjectName(u"groupBox_ScienceObservation")
        self.groupBox_ScienceObservation.setGeometry(QRect(10, 390, 221, 231))
=======
        self.label_temp_detS.setFont(font8)
        self.label_temp_detS.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_temp_detS, 13, 3, 1, 1)

        self.groupBox_ScienceObservation = QGroupBox(Dialog)
        self.groupBox_ScienceObservation.setObjectName(u"groupBox_ScienceObservation")
        self.groupBox_ScienceObservation.setGeometry(QRect(10, 445, 221, 251))
>>>>>>> Stashed changes
        sizePolicy1.setHeightForWidth(self.groupBox_ScienceObservation.sizePolicy().hasHeightForWidth())
        self.groupBox_ScienceObservation.setSizePolicy(sizePolicy1)
        self.groupBox_ScienceObservation.setFont(font)
        self.gridLayout_2 = QGridLayout(self.groupBox_ScienceObservation)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_sampling_number = QLabel(self.groupBox_ScienceObservation)
        self.label_sampling_number.setObjectName(u"label_sampling_number")
        sizePolicy.setHeightForWidth(self.label_sampling_number.sizePolicy().hasHeightForWidth())
        self.label_sampling_number.setSizePolicy(sizePolicy)
<<<<<<< Updated upstream
        self.label_sampling_number.setFont(font4)
=======
        self.label_sampling_number.setFont(font8)
>>>>>>> Stashed changes
        self.label_sampling_number.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_sampling_number, 3, 2, 1, 1)

        self.label_exp_time = QLabel(self.groupBox_ScienceObservation)
        self.label_exp_time.setObjectName(u"label_exp_time")
        sizePolicy.setHeightForWidth(self.label_exp_time.sizePolicy().hasHeightForWidth())
        self.label_exp_time.setSizePolicy(sizePolicy)
<<<<<<< Updated upstream
        self.label_exp_time.setFont(font4)
=======
        self.label_exp_time.setFont(font8)
>>>>>>> Stashed changes
        self.label_exp_time.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_exp_time, 4, 2, 1, 1)

        self.label_g2_4 = QLabel(self.groupBox_ScienceObservation)
        self.label_g2_4.setObjectName(u"label_g2_4")
        sizePolicy.setHeightForWidth(self.label_g2_4.sizePolicy().hasHeightForWidth())
        self.label_g2_4.setSizePolicy(sizePolicy)
        self.label_g2_4.setFont(font7)
        self.label_g2_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_g2_4, 4, 0, 1, 2)

        self.label_g2_5 = QLabel(self.groupBox_ScienceObservation)
        self.label_g2_5.setObjectName(u"label_g2_5")
        sizePolicy.setHeightForWidth(self.label_g2_5.sizePolicy().hasHeightForWidth())
        self.label_g2_5.setSizePolicy(sizePolicy)
        self.label_g2_5.setFont(font7)
        self.label_g2_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_g2_5, 5, 0, 1, 2)

        self.label_g2_6 = QLabel(self.groupBox_ScienceObservation)
        self.label_g2_6.setObjectName(u"label_g2_6")
        sizePolicy.setHeightForWidth(self.label_g2_6.sizePolicy().hasHeightForWidth())
        self.label_g2_6.setSizePolicy(sizePolicy)
        self.label_g2_6.setFont(font7)
        self.label_g2_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_g2_6, 6, 0, 1, 2)

        self.label_data_label = QLabel(self.groupBox_ScienceObservation)
        self.label_data_label.setObjectName(u"label_data_label")
        sizePolicy.setHeightForWidth(self.label_data_label.sizePolicy().hasHeightForWidth())
        self.label_data_label.setSizePolicy(sizePolicy)
        font7 = QFont()
        font7.setPointSize(9)
        font7.setBold(True)
        self.label_data_label.setFont(font7)
        self.label_data_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_data_label, 1, 1, 1, 2)

        self.label_IPA = QLabel(self.groupBox_ScienceObservation)
        self.label_IPA.setObjectName(u"label_IPA")
        sizePolicy.setHeightForWidth(self.label_IPA.sizePolicy().hasHeightForWidth())
        self.label_IPA.setSizePolicy(sizePolicy)
<<<<<<< Updated upstream
        self.label_IPA.setFont(font4)
=======
        self.label_IPA.setFont(font8)
>>>>>>> Stashed changes
        self.label_IPA.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_IPA, 6, 2, 1, 1)

        self.label_time_left = QLabel(self.groupBox_ScienceObservation)
        self.label_time_left.setObjectName(u"label_time_left")
        sizePolicy.setHeightForWidth(self.label_time_left.sizePolicy().hasHeightForWidth())
        self.label_time_left.setSizePolicy(sizePolicy)
<<<<<<< Updated upstream
        self.label_time_left.setFont(font4)
=======
        self.label_time_left.setFont(font8)
>>>>>>> Stashed changes
        self.label_time_left.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_time_left, 5, 2, 1, 1)

        self.label_obs_state = QLabel(self.groupBox_ScienceObservation)
        self.label_obs_state.setObjectName(u"label_obs_state")
        sizePolicy.setHeightForWidth(self.label_obs_state.sizePolicy().hasHeightForWidth())
        self.label_obs_state.setSizePolicy(sizePolicy)
<<<<<<< Updated upstream
        self.label_obs_state.setFont(font4)
=======
        self.label_obs_state.setFont(font8)
>>>>>>> Stashed changes
        self.label_obs_state.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_obs_state, 2, 1, 1, 2)

        self.label_g2 = QLabel(self.groupBox_ScienceObservation)
        self.label_g2.setObjectName(u"label_g2")
        sizePolicy.setHeightForWidth(self.label_g2.sizePolicy().hasHeightForWidth())
        self.label_g2.setSizePolicy(sizePolicy)
        self.label_g2.setFont(font1)
        self.label_g2.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_g2, 0, 0, 1, 3)

        self.label_g2_1 = QLabel(self.groupBox_ScienceObservation)
        self.label_g2_1.setObjectName(u"label_g2_1")
        sizePolicy.setHeightForWidth(self.label_g2_1.sizePolicy().hasHeightForWidth())
        self.label_g2_1.setSizePolicy(sizePolicy)
        self.label_g2_1.setFont(font7)
        self.label_g2_1.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_g2_1, 1, 0, 1, 1)

        self.label_g2_2 = QLabel(self.groupBox_ScienceObservation)
        self.label_g2_2.setObjectName(u"label_g2_2")
        sizePolicy.setHeightForWidth(self.label_g2_2.sizePolicy().hasHeightForWidth())
        self.label_g2_2.setSizePolicy(sizePolicy)
        self.label_g2_2.setFont(font7)
        self.label_g2_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_g2_2, 2, 0, 1, 1)

        self.label_g2_3 = QLabel(self.groupBox_ScienceObservation)
        self.label_g2_3.setObjectName(u"label_g2_3")
        sizePolicy.setHeightForWidth(self.label_g2_3.sizePolicy().hasHeightForWidth())
        self.label_g2_3.setSizePolicy(sizePolicy)
        self.label_g2_3.setFont(font7)
        self.label_g2_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_g2_3, 3, 0, 1, 2)

        self.progressBar_obs = QProgressBar(self.groupBox_ScienceObservation)
        self.progressBar_obs.setObjectName(u"progressBar_obs")
        sizePolicy.setHeightForWidth(self.progressBar_obs.sizePolicy().hasHeightForWidth())
        self.progressBar_obs.setSizePolicy(sizePolicy)
        self.progressBar_obs.setFont(font5)
        self.progressBar_obs.setValue(24)

        self.gridLayout_2.addWidget(self.progressBar_obs, 7, 0, 1, 3)

        self.groupBox_SlitViewCamera = QGroupBox(Dialog)
        self.groupBox_SlitViewCamera.setObjectName(u"groupBox_SlitViewCamera")
        self.groupBox_SlitViewCamera.setGeometry(QRect(580, 10, 301, 255))
        sizePolicy1.setHeightForWidth(self.groupBox_SlitViewCamera.sizePolicy().hasHeightForWidth())
        self.groupBox_SlitViewCamera.setSizePolicy(sizePolicy1)
        self.groupBox_SlitViewCamera.setFont(font)
        self.gridLayout_4 = QGridLayout(self.groupBox_SlitViewCamera)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_svc_filename = QLabel(self.groupBox_SlitViewCamera)
        self.label_svc_filename.setObjectName(u"label_svc_filename")
        sizePolicy.setHeightForWidth(self.label_svc_filename.sizePolicy().hasHeightForWidth())
        self.label_svc_filename.setSizePolicy(sizePolicy)
<<<<<<< Updated upstream
        self.label_svc_filename.setFont(font7)
=======
        self.label_svc_filename.setFont(font6)
>>>>>>> Stashed changes
        self.label_svc_filename.setLayoutDirection(Qt.LeftToRight)
        self.label_svc_filename.setFrameShape(QFrame.StyledPanel)
        self.label_svc_filename.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.label_svc_filename, 1, 2, 1, 4)

        self.bt_single = QPushButton(self.groupBox_SlitViewCamera)
        self.bt_single.setObjectName(u"bt_single")
        sizePolicy.setHeightForWidth(self.bt_single.sizePolicy().hasHeightForWidth())
        self.bt_single.setSizePolicy(sizePolicy)
<<<<<<< Updated upstream
        self.bt_single.setFont(font4)
=======
        self.bt_single.setFont(font8)
>>>>>>> Stashed changes

        self.gridLayout_4.addWidget(self.bt_single, 5, 3, 1, 3)

        self.label_g3_1 = QLabel(self.groupBox_SlitViewCamera)
        self.label_g3_1.setObjectName(u"label_g3_1")
        sizePolicy.setHeightForWidth(self.label_g3_1.sizePolicy().hasHeightForWidth())
        self.label_g3_1.setSizePolicy(sizePolicy)
        self.label_g3_1.setFont(font7)
        self.label_g3_1.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_g3_1, 1, 0, 1, 2)

        self.bt_repeat_filesave = QPushButton(self.groupBox_SlitViewCamera)
        self.bt_repeat_filesave.setObjectName(u"bt_repeat_filesave")
        sizePolicy.setHeightForWidth(self.bt_repeat_filesave.sizePolicy().hasHeightForWidth())
        self.bt_repeat_filesave.setSizePolicy(sizePolicy)
        self.bt_repeat_filesave.setFont(font5)

        self.gridLayout_4.addWidget(self.bt_repeat_filesave, 8, 5, 1, 1)

        self.progressBar_svc = QProgressBar(self.groupBox_SlitViewCamera)
        self.progressBar_svc.setObjectName(u"progressBar_svc")
        sizePolicy.setHeightForWidth(self.progressBar_svc.sizePolicy().hasHeightForWidth())
        self.progressBar_svc.setSizePolicy(sizePolicy)
        self.progressBar_svc.setFont(font5)
        self.progressBar_svc.setValue(24)

        self.gridLayout_4.addWidget(self.progressBar_svc, 6, 0, 1, 6)

        self.e_saving_number = QLineEdit(self.groupBox_SlitViewCamera)
        self.e_saving_number.setObjectName(u"e_saving_number")
        sizePolicy.setHeightForWidth(self.e_saving_number.sizePolicy().hasHeightForWidth())
        self.e_saving_number.setSizePolicy(sizePolicy)
        font8 = QFont()
        font8.setPointSize(16)
        font8.setBold(True)
        self.e_saving_number.setFont(font8)
        self.e_saving_number.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.e_saving_number, 7, 5, 1, 1)

        self.chk_continue = QCheckBox(self.groupBox_SlitViewCamera)
        self.chk_continue.setObjectName(u"chk_continue")
        sizePolicy.setHeightForWidth(self.chk_continue.sizePolicy().hasHeightForWidth())
        self.chk_continue.setSizePolicy(sizePolicy)
        self.chk_continue.setFont(font5)

        self.gridLayout_4.addWidget(self.chk_continue, 5, 0, 1, 2)

        self.label = QLabel(self.groupBox_SlitViewCamera)
        self.label.setObjectName(u"label")
        self.label.setFont(font8)
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label, 7, 4, 1, 1)

        self.chk_auto_save = QCheckBox(self.groupBox_SlitViewCamera)
        self.chk_auto_save.setObjectName(u"chk_auto_save")
        sizePolicy.setHeightForWidth(self.chk_auto_save.sizePolicy().hasHeightForWidth())
        self.chk_auto_save.setSizePolicy(sizePolicy)
        self.chk_auto_save.setFont(font5)

        self.gridLayout_4.addWidget(self.chk_auto_save, 7, 1, 1, 3)

        self.label_g3_3 = QLabel(self.groupBox_SlitViewCamera)
        self.label_g3_3.setObjectName(u"label_g3_3")
        sizePolicy.setHeightForWidth(self.label_g3_3.sizePolicy().hasHeightForWidth())
        self.label_g3_3.setSizePolicy(sizePolicy)
        self.label_g3_3.setFont(font7)
        self.label_g3_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_g3_3, 3, 0, 1, 3)

        self.label_g3_4 = QLabel(self.groupBox_SlitViewCamera)
        self.label_g3_4.setObjectName(u"label_g3_4")
        sizePolicy.setHeightForWidth(self.label_g3_4.sizePolicy().hasHeightForWidth())
        self.label_g3_4.setSizePolicy(sizePolicy)
        self.label_g3_4.setFont(font7)
        self.label_g3_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_g3_4, 4, 0, 1, 3)

        self.label_g3_2 = QLabel(self.groupBox_SlitViewCamera)
        self.label_g3_2.setObjectName(u"label_g3_2")
        sizePolicy.setHeightForWidth(self.label_g3_2.sizePolicy().hasHeightForWidth())
        self.label_g3_2.setSizePolicy(sizePolicy)
        self.label_g3_2.setFont(font7)
        self.label_g3_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_g3_2, 2, 0, 1, 3)

        self.e_svc_fowler_number = QLineEdit(self.groupBox_SlitViewCamera)
        self.e_svc_fowler_number.setObjectName(u"e_svc_fowler_number")
        sizePolicy.setHeightForWidth(self.e_svc_fowler_number.sizePolicy().hasHeightForWidth())
        self.e_svc_fowler_number.setSizePolicy(sizePolicy)
        font9 = QFont()
        font9.setPointSize(8)
        font9.setBold(True)
        self.e_svc_fowler_number.setFont(font9)
        self.e_svc_fowler_number.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.e_svc_fowler_number, 3, 3, 1, 3)

        self.e_svc_exp_time = QLineEdit(self.groupBox_SlitViewCamera)
        self.e_svc_exp_time.setObjectName(u"e_svc_exp_time")
        sizePolicy.setHeightForWidth(self.e_svc_exp_time.sizePolicy().hasHeightForWidth())
        self.e_svc_exp_time.setSizePolicy(sizePolicy)
        self.e_svc_exp_time.setFont(font9)
        self.e_svc_exp_time.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.e_svc_exp_time, 4, 3, 1, 3)

        self.label_svc_state = QLabel(self.groupBox_SlitViewCamera)
        self.label_svc_state.setObjectName(u"label_svc_state")
        sizePolicy.setHeightForWidth(self.label_svc_state.sizePolicy().hasHeightForWidth())
        self.label_svc_state.setSizePolicy(sizePolicy)
<<<<<<< Updated upstream
        self.label_svc_state.setFont(font4)
=======
        self.label_svc_state.setFont(font8)
>>>>>>> Stashed changes
        self.label_svc_state.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_svc_state, 2, 3, 1, 3)

        self.label_g3 = QLabel(self.groupBox_SlitViewCamera)
        self.label_g3.setObjectName(u"label_g3")
        sizePolicy.setHeightForWidth(self.label_g3.sizePolicy().hasHeightForWidth())
        self.label_g3.setSizePolicy(sizePolicy)
        self.label_g3.setFont(font1)
        self.label_g3.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.label_g3, 0, 0, 1, 6)

        self.e_repeat_file_name = QLineEdit(self.groupBox_SlitViewCamera)
        self.e_repeat_file_name.setObjectName(u"e_repeat_file_name")
        sizePolicy.setHeightForWidth(self.e_repeat_file_name.sizePolicy().hasHeightForWidth())
        self.e_repeat_file_name.setSizePolicy(sizePolicy)
        self.e_repeat_file_name.setFont(font9)
        self.e_repeat_file_name.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.e_repeat_file_name, 8, 2, 1, 3)

        self.label_g3_5 = QLabel(self.groupBox_SlitViewCamera)
        self.label_g3_5.setObjectName(u"label_g3_5")
        sizePolicy.setHeightForWidth(self.label_g3_5.sizePolicy().hasHeightForWidth())
        self.label_g3_5.setSizePolicy(sizePolicy)
        self.label_g3_5.setFont(font7)
        self.label_g3_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_g3_5, 8, 0, 1, 2)

        self.groupBox_zscale = QGroupBox(Dialog)
        self.groupBox_zscale.setObjectName(u"groupBox_zscale")
        self.groupBox_zscale.setGeometry(QRect(580, 487, 301, 70))
        sizePolicy1.setHeightForWidth(self.groupBox_zscale.sizePolicy().hasHeightForWidth())
        self.groupBox_zscale.setSizePolicy(sizePolicy1)
        font10 = QFont()
        font10.setPointSize(11)
        self.groupBox_zscale.setFont(font10)
        self.gridLayout_3 = QGridLayout(self.groupBox_zscale)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.radio_zscale = QRadioButton(self.groupBox_zscale)
        self.radio_zscale.setObjectName(u"radio_zscale")
        sizePolicy.setHeightForWidth(self.radio_zscale.sizePolicy().hasHeightForWidth())
        self.radio_zscale.setSizePolicy(sizePolicy)
        self.radio_zscale.setFont(font5)
        self.radio_zscale.setLayoutDirection(Qt.LeftToRight)

        self.gridLayout_3.addWidget(self.radio_zscale, 0, 0, 1, 1)

        self.e_mscale_min = QLineEdit(self.groupBox_zscale)
        self.e_mscale_min.setObjectName(u"e_mscale_min")
        sizePolicy.setHeightForWidth(self.e_mscale_min.sizePolicy().hasHeightForWidth())
        self.e_mscale_min.setSizePolicy(sizePolicy)
        self.e_mscale_min.setFont(font9)
        self.e_mscale_min.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.e_mscale_min, 1, 1, 1, 1)

        self.e_mscale_max = QLineEdit(self.groupBox_zscale)
        self.e_mscale_max.setObjectName(u"e_mscale_max")
        sizePolicy.setHeightForWidth(self.e_mscale_max.sizePolicy().hasHeightForWidth())
        self.e_mscale_max.setSizePolicy(sizePolicy)
        self.e_mscale_max.setFont(font9)
        self.e_mscale_max.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.e_mscale_max, 1, 2, 1, 1)

        self.radio_mscale = QRadioButton(self.groupBox_zscale)
        self.radio_mscale.setObjectName(u"radio_mscale")
        sizePolicy.setHeightForWidth(self.radio_mscale.sizePolicy().hasHeightForWidth())
        self.radio_mscale.setSizePolicy(sizePolicy)
        self.radio_mscale.setFont(font5)
        self.radio_mscale.setLayoutDirection(Qt.LeftToRight)

        self.gridLayout_3.addWidget(self.radio_mscale, 1, 0, 1, 1)

        self.label_zscale = QLabel(self.groupBox_zscale)
        self.label_zscale.setObjectName(u"label_zscale")
        sizePolicy.setHeightForWidth(self.label_zscale.sizePolicy().hasHeightForWidth())
        self.label_zscale.setSizePolicy(sizePolicy)
<<<<<<< Updated upstream
        self.label_zscale.setFont(font4)
=======
        self.label_zscale.setFont(font8)
>>>>>>> Stashed changes
        self.label_zscale.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_zscale, 0, 1, 1, 2)

        self.label_messagebar = QLabel(Dialog)
        self.label_messagebar.setObjectName(u"label_messagebar")
        self.label_messagebar.setGeometry(QRect(50, 700, 521, 25))
        sizePolicy.setHeightForWidth(self.label_messagebar.sizePolicy().hasHeightForWidth())
        self.label_messagebar.setSizePolicy(sizePolicy)
        font11 = QFont()
        font11.setBold(True)
        self.label_messagebar.setFont(font11)
        self.label_messagebar.setAlignment(Qt.AlignCenter)
        self.frame_expand = QFrame(Dialog)
        self.frame_expand.setObjectName(u"frame_expand")
        self.frame_expand.setGeometry(QRect(230, 4, 181, 181))
        sizePolicy.setHeightForWidth(self.frame_expand.sizePolicy().hasHeightForWidth())
        self.frame_expand.setSizePolicy(sizePolicy)
        self.frame_expand.setCursor(QCursor(Qt.ArrowCursor))
        self.frame_expand.setMouseTracking(False)
        self.frame_expand.setLayoutDirection(Qt.LeftToRight)
        self.frame_expand.setFrameShape(QFrame.NoFrame)
        self.frame_expand.setFrameShadow(QFrame.Raised)
        self.frame_fitting = QFrame(Dialog)
        self.frame_fitting.setObjectName(u"frame_fitting")
        self.frame_fitting.setEnabled(True)
        self.frame_fitting.setGeometry(QRect(400, 4, 181, 181))
        sizePolicy2 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(2)
        sizePolicy2.setHeightForWidth(self.frame_fitting.sizePolicy().hasHeightForWidth())
        self.frame_fitting.setSizePolicy(sizePolicy2)
        self.frame_fitting.setCursor(QCursor(Qt.ArrowCursor))
        self.frame_fitting.setMouseTracking(False)
        self.frame_fitting.setFrameShape(QFrame.NoFrame)
        self.frame_fitting.setFrameShadow(QFrame.Raised)
        self.frame_svc = QFrame(Dialog)
        self.frame_svc.setObjectName(u"frame_svc")
        self.frame_svc.setEnabled(True)
        self.frame_svc.setGeometry(QRect(230, 170, 351, 351))
        sizePolicy.setHeightForWidth(self.frame_svc.sizePolicy().hasHeightForWidth())
        self.frame_svc.setSizePolicy(sizePolicy)
        self.frame_svc.setCursor(QCursor(Qt.ArrowCursor))
        self.frame_svc.setMouseTracking(False)
        self.frame_svc.setAutoFillBackground(False)
        self.frame_svc.setFrameShape(QFrame.NoFrame)
        self.frame_svc.setFrameShadow(QFrame.Raised)
        self.radio_none = QRadioButton(Dialog)
        self.radio_none.setObjectName(u"radio_none")
        self.radio_none.setEnabled(True)
<<<<<<< Updated upstream
        self.radio_none.setGeometry(QRect(560, 630, 61, 25))
        self.radio_none.setFont(font5)
        self.radio_show_logfile = QRadioButton(Dialog)
        self.radio_show_logfile.setObjectName(u"radio_show_logfile")
        self.radio_show_logfile.setGeometry(QRect(620, 630, 111, 25))
        self.radio_show_logfile.setFont(font5)
        self.radio_show_loglist = QRadioButton(Dialog)
        self.radio_show_loglist.setObjectName(u"radio_show_loglist")
        self.radio_show_loglist.setGeometry(QRect(730, 630, 111, 25))
=======
        self.radio_none.setGeometry(QRect(580, 700, 61, 25))
        self.radio_none.setFont(font5)
        self.radio_show_logfile = QRadioButton(Dialog)
        self.radio_show_logfile.setObjectName(u"radio_show_logfile")
        self.radio_show_logfile.setGeometry(QRect(650, 700, 116, 25))
        self.radio_show_logfile.setFont(font5)
        self.radio_show_loglist = QRadioButton(Dialog)
        self.radio_show_loglist.setObjectName(u"radio_show_loglist")
        self.radio_show_loglist.setGeometry(QRect(770, 700, 116, 25))
>>>>>>> Stashed changes
        self.radio_show_loglist.setFont(font5)
        self.groupBox_profile = QGroupBox(Dialog)
        self.groupBox_profile.setObjectName(u"groupBox_profile")
        self.groupBox_profile.setGeometry(QRect(580, 564, 301, 131))
        sizePolicy.setHeightForWidth(self.groupBox_profile.sizePolicy().hasHeightForWidth())
        self.groupBox_profile.setSizePolicy(sizePolicy)
        self.frame_profile = QFrame(self.groupBox_profile)
        self.frame_profile.setObjectName(u"frame_profile")
        self.frame_profile.setGeometry(QRect(2, 9, 301, 111))
        sizePolicy.setHeightForWidth(self.frame_profile.sizePolicy().hasHeightForWidth())
        self.frame_profile.setSizePolicy(sizePolicy)
        self.frame_profile.setCursor(QCursor(Qt.ArrowCursor))
        self.frame_profile.setMouseTracking(False)
        self.frame_profile.setFrameShape(QFrame.NoFrame)
        self.frame_profile.setFrameShadow(QFrame.Raised)
        self.label_star_slit = QLabel(self.groupBox_profile)
        self.label_star_slit.setObjectName(u"label_star_slit")
        self.label_star_slit.setGeometry(QRect(196, 110, 42, 19))
        self.label_sw_star = QLabel(self.groupBox_profile)
        self.label_sw_star.setObjectName(u"label_sw_star")
        self.label_sw_star.setGeometry(QRect(134, 110, 61, 20))
        self.label_sw_slit = QLabel(self.groupBox_profile)
        self.label_sw_slit.setObjectName(u"label_sw_slit")
        self.label_sw_slit.setGeometry(QRect(36, 110, 61, 20))
        self.label_sw_star_slit = QLabel(self.groupBox_profile)
        self.label_sw_star_slit.setObjectName(u"label_sw_star_slit")
        self.label_sw_star_slit.setGeometry(QRect(238, 110, 61, 20))
        sizePolicy.setHeightForWidth(self.label_sw_star_slit.sizePolicy().hasHeightForWidth())
        self.label_sw_star_slit.setSizePolicy(sizePolicy)
        self.label_slit = QLabel(self.groupBox_profile)
        self.label_slit.setObjectName(u"label_slit")
        self.label_slit.setGeometry(QRect(6, 110, 28, 19))
        self.label_star = QLabel(self.groupBox_profile)
        self.label_star.setObjectName(u"label_star")
        self.label_star.setGeometry(QRect(98, 110, 33, 19))
        self.groupBox_withTCS = QGroupBox(Dialog)
        self.groupBox_withTCS.setObjectName(u"groupBox_withTCS")
        self.groupBox_withTCS.setGeometry(QRect(580, 272, 301, 150))
        self.groupBox_withTCS.setFlat(False)
<<<<<<< Updated upstream
        self.gridLayout_5 = QGridLayout(self.groupBox_withTCS)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_cur_Idx = QLabel(self.groupBox_withTCS)
        self.label_cur_Idx.setObjectName(u"label_cur_Idx")
        self.label_cur_Idx.setFont(font8)
        self.label_cur_Idx.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_cur_Idx, 5, 4, 1, 1)

        self.e_averaging_number = QLineEdit(self.groupBox_withTCS)
        self.e_averaging_number.setObjectName(u"e_averaging_number")
        sizePolicy.setHeightForWidth(self.e_averaging_number.sizePolicy().hasHeightForWidth())
        self.e_averaging_number.setSizePolicy(sizePolicy)
        self.e_averaging_number.setFont(font8)
        self.e_averaging_number.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.e_averaging_number, 5, 5, 1, 1)

        self.bt_minus_p = QPushButton(self.groupBox_withTCS)
        self.bt_minus_p.setObjectName(u"bt_minus_p")
        sizePolicy.setHeightForWidth(self.bt_minus_p.sizePolicy().hasHeightForWidth())
        self.bt_minus_p.setSizePolicy(sizePolicy)
        self.bt_minus_p.setFont(font4)
=======
        self.gridLayout = QGridLayout(self.groupBox_withTCS)
        self.gridLayout.setObjectName(u"gridLayout")
        self.bt_plus_p = QPushButton(self.groupBox_withTCS)
        self.bt_plus_p.setObjectName(u"bt_plus_p")
        sizePolicy.setHeightForWidth(self.bt_plus_p.sizePolicy().hasHeightForWidth())
        self.bt_plus_p.setSizePolicy(sizePolicy)
        self.bt_plus_p.setFont(font8)
>>>>>>> Stashed changes

        self.gridLayout.addWidget(self.bt_plus_p, 0, 1, 1, 1)

<<<<<<< Updated upstream
        self.bt_center = QPushButton(self.groupBox_withTCS)
        self.bt_center.setObjectName(u"bt_center")
        sizePolicy.setHeightForWidth(self.bt_center.sizePolicy().hasHeightForWidth())
        self.bt_center.setSizePolicy(sizePolicy)
        self.bt_center.setFont(font4)
=======
        self.bt_minus_q = QPushButton(self.groupBox_withTCS)
        self.bt_minus_q.setObjectName(u"bt_minus_q")
        sizePolicy.setHeightForWidth(self.bt_minus_q.sizePolicy().hasHeightForWidth())
        self.bt_minus_q.setSizePolicy(sizePolicy)
        self.bt_minus_q.setFont(font8)
>>>>>>> Stashed changes

        self.gridLayout.addWidget(self.bt_minus_q, 1, 0, 1, 1)

        self.bt_plus_q = QPushButton(self.groupBox_withTCS)
        self.bt_plus_q.setObjectName(u"bt_plus_q")
        sizePolicy.setHeightForWidth(self.bt_plus_q.sizePolicy().hasHeightForWidth())
        self.bt_plus_q.setSizePolicy(sizePolicy)
<<<<<<< Updated upstream
        self.bt_plus_q.setFont(font4)

        self.gridLayout_5.addWidget(self.bt_plus_q, 3, 2, 1, 1)

        self.bt_slow_guide = QPushButton(self.groupBox_withTCS)
        self.bt_slow_guide.setObjectName(u"bt_slow_guide")
        sizePolicy.setHeightForWidth(self.bt_slow_guide.sizePolicy().hasHeightForWidth())
        self.bt_slow_guide.setSizePolicy(sizePolicy)
        self.bt_slow_guide.setFont(font4)

        self.gridLayout_5.addWidget(self.bt_slow_guide, 5, 0, 1, 4)
=======
        self.bt_plus_q.setFont(font8)

        self.gridLayout.addWidget(self.bt_plus_q, 1, 2, 1, 1)
>>>>>>> Stashed changes

        self.label_g3_6 = QLabel(self.groupBox_withTCS)
        self.label_g3_6.setObjectName(u"label_g3_6")
        sizePolicy.setHeightForWidth(self.label_g3_6.sizePolicy().hasHeightForWidth())
        self.label_g3_6.setSizePolicy(sizePolicy)
        self.label_g3_6.setFont(font7)
        self.label_g3_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

<<<<<<< Updated upstream
        self.gridLayout_5.addWidget(self.label_g3_6, 3, 3, 1, 2)

        self.radio_cross = QRadioButton(self.groupBox_withTCS)
        self.radio_cross.setObjectName(u"radio_cross")
        self.radio_cross.setFont(font5)
        self.radio_cross.setAutoExclusive(True)

        self.gridLayout_5.addWidget(self.radio_cross, 0, 4, 1, 2)

        self.radio_centroid = QRadioButton(self.groupBox_withTCS)
        self.radio_centroid.setObjectName(u"radio_centroid")
        self.radio_centroid.setFont(font5)
        self.radio_centroid.setAutoExclusive(True)

        self.gridLayout_5.addWidget(self.radio_centroid, 0, 2, 1, 2)
=======
        self.gridLayout.addWidget(self.label_g3_6, 1, 3, 1, 2)
>>>>>>> Stashed changes

        self.e_offset = QLineEdit(self.groupBox_withTCS)
        self.e_offset.setObjectName(u"e_offset")
        sizePolicy.setHeightForWidth(self.e_offset.sizePolicy().hasHeightForWidth())
        self.e_offset.setSizePolicy(sizePolicy)
<<<<<<< Updated upstream
        self.e_offset.setFont(font4)
=======
        self.e_offset.setFont(font8)
>>>>>>> Stashed changes
        self.e_offset.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.e_offset, 1, 5, 1, 1)

<<<<<<< Updated upstream
        self.chk_off_slit = QCheckBox(self.groupBox_withTCS)
        self.chk_off_slit.setObjectName(u"chk_off_slit")
        sizePolicy.setHeightForWidth(self.chk_off_slit.sizePolicy().hasHeightForWidth())
        self.chk_off_slit.setSizePolicy(sizePolicy)
        self.chk_off_slit.setFont(font5)
=======
        self.bt_minus_p = QPushButton(self.groupBox_withTCS)
        self.bt_minus_p.setObjectName(u"bt_minus_p")
        sizePolicy.setHeightForWidth(self.bt_minus_p.sizePolicy().hasHeightForWidth())
        self.bt_minus_p.setSizePolicy(sizePolicy)
        self.bt_minus_p.setFont(font8)
>>>>>>> Stashed changes

        self.gridLayout.addWidget(self.bt_minus_p, 2, 1, 1, 1)

<<<<<<< Updated upstream
        self.bt_set_guide_star = QPushButton(self.groupBox_withTCS)
        self.bt_set_guide_star.setObjectName(u"bt_set_guide_star")
        sizePolicy.setHeightForWidth(self.bt_set_guide_star.sizePolicy().hasHeightForWidth())
        self.bt_set_guide_star.setSizePolicy(sizePolicy)
        self.bt_set_guide_star.setFont(font4)
=======
        self.bt_slow_guide = QPushButton(self.groupBox_withTCS)
        self.bt_slow_guide.setObjectName(u"bt_slow_guide")
        sizePolicy.setHeightForWidth(self.bt_slow_guide.sizePolicy().hasHeightForWidth())
        self.bt_slow_guide.setSizePolicy(sizePolicy)
        self.bt_slow_guide.setFont(font8)
>>>>>>> Stashed changes

        self.gridLayout.addWidget(self.bt_slow_guide, 3, 0, 1, 4)

<<<<<<< Updated upstream
        self.bt_minus_q = QPushButton(self.groupBox_withTCS)
        self.bt_minus_q.setObjectName(u"bt_minus_q")
        sizePolicy.setHeightForWidth(self.bt_minus_q.sizePolicy().hasHeightForWidth())
        self.bt_minus_q.setSizePolicy(sizePolicy)
        self.bt_minus_q.setFont(font4)
=======
        self.label_cur_Idx = QLabel(self.groupBox_withTCS)
        self.label_cur_Idx.setObjectName(u"label_cur_Idx")
        self.label_cur_Idx.setFont(font10)
        self.label_cur_Idx.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
>>>>>>> Stashed changes

        self.gridLayout.addWidget(self.label_cur_Idx, 3, 4, 1, 1)

<<<<<<< Updated upstream
        self.bt_plus_p = QPushButton(self.groupBox_withTCS)
        self.bt_plus_p.setObjectName(u"bt_plus_p")
        sizePolicy.setHeightForWidth(self.bt_plus_p.sizePolicy().hasHeightForWidth())
        self.bt_plus_p.setSizePolicy(sizePolicy)
        self.bt_plus_p.setFont(font4)
=======
        self.e_averaging_number = QLineEdit(self.groupBox_withTCS)
        self.e_averaging_number.setObjectName(u"e_averaging_number")
        sizePolicy.setHeightForWidth(self.e_averaging_number.sizePolicy().hasHeightForWidth())
        self.e_averaging_number.setSizePolicy(sizePolicy)
        self.e_averaging_number.setFont(font10)
        self.e_averaging_number.setAlignment(Qt.AlignCenter)
>>>>>>> Stashed changes

        self.gridLayout.addWidget(self.e_averaging_number, 3, 5, 1, 1)

        self.groupBox_view = QGroupBox(Dialog)
        self.groupBox_view.setObjectName(u"groupBox_view")
        self.groupBox_view.setGeometry(QRect(580, 429, 301, 51))
        self.gridLayout_6 = QGridLayout(self.groupBox_view)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
<<<<<<< Updated upstream
        self.chk_view_drawing = QCheckBox(self.groupBox_view)
        self.chk_view_drawing.setObjectName(u"chk_view_drawing")
        self.chk_view_drawing.setFont(font5)
=======
        self.bt_mark_sky = QPushButton(self.groupBox_view)
        self.bt_mark_sky.setObjectName(u"bt_mark_sky")
        sizePolicy.setHeightForWidth(self.bt_mark_sky.sizePolicy().hasHeightForWidth())
        self.bt_mark_sky.setSizePolicy(sizePolicy)
        self.bt_mark_sky.setFont(font6)

        self.gridLayout_6.addWidget(self.bt_mark_sky, 0, 2, 1, 1)
>>>>>>> Stashed changes

        self.radio_sub = QRadioButton(self.groupBox_view)
        self.radio_sub.setObjectName(u"radio_sub")
        sizePolicy.setHeightForWidth(self.radio_sub.sizePolicy().hasHeightForWidth())
        self.radio_sub.setSizePolicy(sizePolicy)
        font13 = QFont()
        font13.setPointSize(9)
        self.radio_sub.setFont(font13)
        self.radio_sub.setLayoutDirection(Qt.LeftToRight)
        self.radio_sub.setAutoExclusive(True)

        self.gridLayout_6.addWidget(self.radio_sub, 0, 1, 1, 1)

        self.radio_raw = QRadioButton(self.groupBox_view)
        self.radio_raw.setObjectName(u"radio_raw")
        sizePolicy.setHeightForWidth(self.radio_raw.sizePolicy().hasHeightForWidth())
        self.radio_raw.setSizePolicy(sizePolicy)
<<<<<<< Updated upstream
        font12 = QFont()
        font12.setFamilies([u"Courier 10 Pitch"])
        font12.setPointSize(10)
        self.radio_raw.setFont(font12)
=======
        font14 = QFont()
        font14.setFamilies([u"Cantarell"])
        font14.setPointSize(10)
        self.radio_raw.setFont(font14)
>>>>>>> Stashed changes
        self.radio_raw.setLayoutDirection(Qt.LeftToRight)
        self.radio_raw.setAutoExclusive(True)

        self.gridLayout_6.addWidget(self.radio_raw, 0, 0, 1, 1)

        self.frame_svc_expand = QFrame(Dialog)
        self.frame_svc_expand.setObjectName(u"frame_svc_expand")
        self.frame_svc_expand.setEnabled(True)
        self.frame_svc_expand.setGeometry(QRect(230, 505, 201, 201))
        sizePolicy.setHeightForWidth(self.frame_svc_expand.sizePolicy().hasHeightForWidth())
        self.frame_svc_expand.setSizePolicy(sizePolicy)
        self.frame_svc_expand.setCursor(QCursor(Qt.ArrowCursor))
        self.frame_svc_expand.setMouseTracking(False)
        self.frame_svc_expand.setAutoFillBackground(False)
        self.frame_svc_expand.setFrameShape(QFrame.NoFrame)
        self.frame_svc_expand.setFrameShadow(QFrame.Raised)
        self.groupBox_withView = QGroupBox(Dialog)
        self.groupBox_withView.setObjectName(u"groupBox_withView")
        self.groupBox_withView.setGeometry(QRect(400, 515, 171, 181))
        self.groupBox_withView.setFlat(False)
        self.gridLayout_5 = QGridLayout(self.groupBox_withView)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_2 = QLabel(self.groupBox_withView)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font13)
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

<<<<<<< Updated upstream
        self.radio_sub = QRadioButton(self.groupBox_view)
        self.radio_sub.setObjectName(u"radio_sub")
        sizePolicy.setHeightForWidth(self.radio_sub.sizePolicy().hasHeightForWidth())
        self.radio_sub.setSizePolicy(sizePolicy)
        self.radio_sub.setFont(font5)
        self.radio_sub.setLayoutDirection(Qt.LeftToRight)
        self.radio_sub.setAutoExclusive(True)
=======
        self.gridLayout_5.addWidget(self.label_2, 0, 0, 1, 1)
>>>>>>> Stashed changes

        self.cmb_view_scale = QComboBox(self.groupBox_withView)
        self.cmb_view_scale.addItem("")
        self.cmb_view_scale.addItem("")
        self.cmb_view_scale.addItem("")
        self.cmb_view_scale.addItem("")
        self.cmb_view_scale.setObjectName(u"cmb_view_scale")
        self.cmb_view_scale.setFont(font5)

<<<<<<< Updated upstream
        self.bt_mark_sky = QPushButton(self.groupBox_view)
        self.bt_mark_sky.setObjectName(u"bt_mark_sky")
        sizePolicy.setHeightForWidth(self.bt_mark_sky.sizePolicy().hasHeightForWidth())
        self.bt_mark_sky.setSizePolicy(sizePolicy)
        self.bt_mark_sky.setFont(font7)
=======
        self.gridLayout_5.addWidget(self.cmb_view_scale, 0, 1, 1, 1)

        self.chk_view_drawing = QCheckBox(self.groupBox_withView)
        self.chk_view_drawing.setObjectName(u"chk_view_drawing")
        self.chk_view_drawing.setFont(font13)

        self.gridLayout_5.addWidget(self.chk_view_drawing, 0, 2, 1, 1)

        self.radio_centroid = QRadioButton(self.groupBox_withView)
        self.radio_centroid.setObjectName(u"radio_centroid")
        self.radio_centroid.setFont(font5)
        self.radio_centroid.setAutoExclusive(True)

        self.gridLayout_5.addWidget(self.radio_centroid, 1, 0, 1, 2)
>>>>>>> Stashed changes

        self.radio_cross = QRadioButton(self.groupBox_withView)
        self.radio_cross.setObjectName(u"radio_cross")
        self.radio_cross.setFont(font5)
        self.radio_cross.setAutoExclusive(True)

        self.gridLayout_5.addWidget(self.radio_cross, 1, 2, 1, 1)

        self.chk_off_slit = QCheckBox(self.groupBox_withView)
        self.chk_off_slit.setObjectName(u"chk_off_slit")
        sizePolicy.setHeightForWidth(self.chk_off_slit.sizePolicy().hasHeightForWidth())
        self.chk_off_slit.setSizePolicy(sizePolicy)
        self.chk_off_slit.setFont(font5)

        self.gridLayout_5.addWidget(self.chk_off_slit, 3, 0, 1, 3)

        self.bt_set_guide_star = QPushButton(self.groupBox_withView)
        self.bt_set_guide_star.setObjectName(u"bt_set_guide_star")
        sizePolicy.setHeightForWidth(self.bt_set_guide_star.sizePolicy().hasHeightForWidth())
        self.bt_set_guide_star.setSizePolicy(sizePolicy)
        self.bt_set_guide_star.setFont(font8)

        self.gridLayout_5.addWidget(self.bt_set_guide_star, 4, 0, 1, 3)

        self.bt_center = QPushButton(self.groupBox_withView)
        self.bt_center.setObjectName(u"bt_center")
        sizePolicy.setHeightForWidth(self.bt_center.sizePolicy().hasHeightForWidth())
        self.bt_center.setSizePolicy(sizePolicy)
        self.bt_center.setFont(font8)

        self.gridLayout_5.addWidget(self.bt_center, 2, 0, 1, 3)

        self.pushButton_help = QPushButton(Dialog)
        self.pushButton_help.setObjectName(u"pushButton_help")
        self.pushButton_help.setGeometry(QRect(10, 700, 41, 27))
        QWidget.setTabOrder(self.e_svc_fowler_number, self.chk_continue)
        QWidget.setTabOrder(self.chk_continue, self.bt_single)
        QWidget.setTabOrder(self.bt_single, self.chk_auto_save)
        QWidget.setTabOrder(self.chk_auto_save, self.e_saving_number)
        QWidget.setTabOrder(self.e_saving_number, self.e_repeat_file_name)
        QWidget.setTabOrder(self.e_repeat_file_name, self.bt_repeat_filesave)
        QWidget.setTabOrder(self.bt_repeat_filesave, self.radio_zscale)
        QWidget.setTabOrder(self.radio_zscale, self.radio_mscale)
        QWidget.setTabOrder(self.radio_mscale, self.e_mscale_min)
        QWidget.setTabOrder(self.e_mscale_min, self.e_mscale_max)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.groupBox_InstrumentStatus.setTitle("")
        self.label_g1.setText(QCoreApplication.translate("Dialog", u"Instrument Status", None))
        self.label_heartbeat.setText(QCoreApplication.translate("Dialog", u"\u2665", None))
<<<<<<< Updated upstream
        self.label_g1_1.setText(QCoreApplication.translate("Dialog", u"IGRINS-2:", None))
        self.label_is_health.setText(QCoreApplication.translate("Dialog", u"GOOD", None))
=======
        self.label_g1_1.setText(QCoreApplication.translate("Dialog", u"IGRINS-2", None))
        self.label_heartbeat_ics.setText(QCoreApplication.translate("Dialog", u"\u2665", None))
>>>>>>> Stashed changes
        self.label_g1_13.setText(QCoreApplication.translate("Dialog", u"ICS:", None))
        self.label_ics_health.setText(QCoreApplication.translate("Dialog", u"GOOD", None))
        self.label_g1_14.setText(QCoreApplication.translate("Dialog", u"DCSH:", None))
        self.label_dcsh_health.setText(QCoreApplication.translate("Dialog", u"GOOD", None))
        self.label_g1_15.setText(QCoreApplication.translate("Dialog", u"DCSK:", None))
        self.label_dcsk_health.setText(QCoreApplication.translate("Dialog", u"GOOD", None))
        self.label_g1_24.setText(QCoreApplication.translate("Dialog", u"DCSS:", None))
        self.label_dcss_health.setText(QCoreApplication.translate("Dialog", u"GOOD", None))
        self.label_g1_2.setText(QCoreApplication.translate("Dialog", u"GDSN Status:", None))
        self.label_GDSN_connection.setText(QCoreApplication.translate("Dialog", u"Disconnected", None))
        self.label_g1_3.setText(QCoreApplication.translate("Dialog", u"GMP Status:", None))
        self.label_GMP_connection.setText(QCoreApplication.translate("Dialog", u"Disconnected", None))
        self.label_g1_4.setText(QCoreApplication.translate("Dialog", u"State:", None))
        self.label_state.setText(QCoreApplication.translate("Dialog", u"Running", None))
        self.label_g1_5.setText(QCoreApplication.translate("Dialog", u"Action State:", None))
        self.label_action_state.setText(QCoreApplication.translate("Dialog", u"Idle", None))
<<<<<<< Updated upstream
        self.label_g1_7.setText(QCoreApplication.translate("Dialog", u"Det H (K):", None))
        self.label_temp_detH.setText(QCoreApplication.translate("Dialog", u"65.0", None))
        self.label_g1_8.setText(QCoreApplication.translate("Dialog", u"Det K (K):", None))
        self.label_temp_detK.setText(QCoreApplication.translate("Dialog", u"65.0", None))
        self.label_g1_9.setText(QCoreApplication.translate("Dialog", u"Det S (K):", None))
=======
        self.label_g1_7.setText(QCoreApplication.translate("Dialog", u"Detector H (K):", None))
        self.label_temp_detH.setText(QCoreApplication.translate("Dialog", u"65.0", None))
        self.label_g1_8.setText(QCoreApplication.translate("Dialog", u"Detector K (K):", None))
        self.label_temp_detK.setText(QCoreApplication.translate("Dialog", u"65.0", None))
        self.label_g1_9.setText(QCoreApplication.translate("Dialog", u"Detector S (K):", None))
>>>>>>> Stashed changes
        self.label_temp_detS.setText(QCoreApplication.translate("Dialog", u"65.0", None))
        self.groupBox_ScienceObservation.setTitle("")
        self.label_sampling_number.setText(QCoreApplication.translate("Dialog", u"16", None))
        self.label_exp_time.setText(QCoreApplication.translate("Dialog", u"123456.32", None))
        self.label_g2_4.setText(QCoreApplication.translate("Dialog", u"Exposure Time (sec):", None))
        self.label_g2_5.setText(QCoreApplication.translate("Dialog", u"Time Left:", None))
        self.label_g2_6.setText(QCoreApplication.translate("Dialog", u"IPA (deg):", None))
        self.label_data_label.setText(QCoreApplication.translate("Dialog", u"S20221020S0001", None))
        self.label_IPA.setText(QCoreApplication.translate("Dialog", u"90", None))
        self.label_time_left.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.label_obs_state.setText(QCoreApplication.translate("Dialog", u"---", None))
        self.label_g2.setText(QCoreApplication.translate("Dialog", u"Science Observation", None))
        self.label_g2_1.setText(QCoreApplication.translate("Dialog", u"Data Label:", None))
        self.label_g2_2.setText(QCoreApplication.translate("Dialog", u"Observing State:", None))
        self.label_g2_3.setText(QCoreApplication.translate("Dialog", u"Fowler Sampling:", None))
        self.groupBox_SlitViewCamera.setTitle("")
        self.label_svc_filename.setText(QCoreApplication.translate("Dialog", u"SDCS_20240105_0004.fits", None))
        self.bt_single.setText(QCoreApplication.translate("Dialog", u"Exposure", None))
        self.label_g3_1.setText(QCoreApplication.translate("Dialog", u"File Name:", None))
        self.bt_repeat_filesave.setText(QCoreApplication.translate("Dialog", u"save", None))
        self.e_saving_number.setText(QCoreApplication.translate("Dialog", u"5", None))
        self.chk_continue.setText(QCoreApplication.translate("Dialog", u"continue", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"1 /", None))
        self.chk_auto_save.setText(QCoreApplication.translate("Dialog", u"Auto save (local)", None))
        self.label_g3_3.setText(QCoreApplication.translate("Dialog", u"Fowler Sampling:", None))
        self.label_g3_4.setText(QCoreApplication.translate("Dialog", u"Exposure Time (sec):", None))
        self.label_g3_2.setText(QCoreApplication.translate("Dialog", u"Observing State:", None))
        self.label_svc_state.setText(QCoreApplication.translate("Dialog", u"---", None))
        self.label_g3.setText(QCoreApplication.translate("Dialog", u"Slit View Camera", None))
        self.e_repeat_file_name.setText("")
        self.label_g3_5.setText(QCoreApplication.translate("Dialog", u"File name:", None))
        self.groupBox_zscale.setTitle("")
        self.radio_zscale.setText(QCoreApplication.translate("Dialog", u"zscale", None))
        self.radio_mscale.setText(QCoreApplication.translate("Dialog", u"manual", None))
        self.label_zscale.setText(QCoreApplication.translate("Dialog", u"10 ~ 500", None))
        self.label_messagebar.setText(QCoreApplication.translate("Dialog", u"TextLabel", None))
        self.radio_none.setText(QCoreApplication.translate("Dialog", u"None", None))
        self.radio_show_logfile.setText(QCoreApplication.translate("Dialog", u"Open \"log file\"", None))
        self.radio_show_loglist.setText(QCoreApplication.translate("Dialog", u"Open \"log list\"", None))
        self.groupBox_profile.setTitle("")
        self.label_star_slit.setText(QCoreApplication.translate("Dialog", u"star* :", None))
        self.label_sw_star.setText(QCoreApplication.translate("Dialog", u"-", None))
        self.label_sw_slit.setText(QCoreApplication.translate("Dialog", u"-", None))
        self.label_sw_star_slit.setText(QCoreApplication.translate("Dialog", u"-", None))
        self.label_slit.setText(QCoreApplication.translate("Dialog", u"slit :", None))
        self.label_star.setText(QCoreApplication.translate("Dialog", u"star :", None))
        self.groupBox_withTCS.setTitle("")
        self.bt_plus_p.setText(QCoreApplication.translate("Dialog", u"+p", None))
        self.bt_minus_q.setText(QCoreApplication.translate("Dialog", u"-q", None))
        self.bt_plus_q.setText(QCoreApplication.translate("Dialog", u"+q", None))
        self.label_g3_6.setText(QCoreApplication.translate("Dialog", u"Offset(\") =", None))
        self.bt_minus_p.setText(QCoreApplication.translate("Dialog", u"-p", None))
        self.bt_slow_guide.setText(QCoreApplication.translate("Dialog", u"Slow Guide", None))
        self.label_cur_Idx.setText(QCoreApplication.translate("Dialog", u"1 /", None))
        self.e_averaging_number.setText(QCoreApplication.translate("Dialog", u"5", None))
        self.groupBox_view.setTitle("")
        self.bt_mark_sky.setText(QCoreApplication.translate("Dialog", u"Mark Sky", None))
        self.radio_sub.setText(QCoreApplication.translate("Dialog", u"Sub(Sky)", None))
        self.radio_raw.setText(QCoreApplication.translate("Dialog", u"Raw", None))
        self.groupBox_withView.setTitle("")
        self.label_2.setText(QCoreApplication.translate("Dialog", u"zoom", None))
        self.cmb_view_scale.setItemText(0, QCoreApplication.translate("Dialog", u"1", None))
        self.cmb_view_scale.setItemText(1, QCoreApplication.translate("Dialog", u"2", None))
        self.cmb_view_scale.setItemText(2, QCoreApplication.translate("Dialog", u"3", None))
        self.cmb_view_scale.setItemText(3, QCoreApplication.translate("Dialog", u"4", None))

        self.chk_view_drawing.setText(QCoreApplication.translate("Dialog", u"Box On", None))
        self.radio_centroid.setText(QCoreApplication.translate("Dialog", u"Centroid", None))
        self.radio_cross.setText(QCoreApplication.translate("Dialog", u"Cross", None))
        self.chk_off_slit.setText(QCoreApplication.translate("Dialog", u"Off-slit Guide", None))
        self.bt_set_guide_star.setText(QCoreApplication.translate("Dialog", u"Set Guide star", None))
<<<<<<< Updated upstream
        self.bt_minus_q.setText(QCoreApplication.translate("Dialog", u"-q", None))
        self.bt_plus_p.setText(QCoreApplication.translate("Dialog", u"+p", None))
        self.groupBox_view.setTitle("")
        self.chk_view_drawing.setText(QCoreApplication.translate("Dialog", u"View", None))
        self.radio_raw.setText(QCoreApplication.translate("Dialog", u"Raw", None))
        self.radio_sub.setText(QCoreApplication.translate("Dialog", u"Sub (Sky)", None))
        self.bt_mark_sky.setText(QCoreApplication.translate("Dialog", u"Mark Sky", None))
=======
        self.bt_center.setText(QCoreApplication.translate("Dialog", u"Center", None))
        self.pushButton_help.setText(QCoreApplication.translate("Dialog", u"Help", None))
>>>>>>> Stashed changes
    # retranslateUi

