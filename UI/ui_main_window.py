# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QLayout, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QVBoxLayout, QWidget)
import jeff_profile_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(400, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 381, 551))
        self.main_window_v_layout = QVBoxLayout(self.verticalLayoutWidget)
        self.main_window_v_layout.setObjectName(u"main_window_v_layout")
        self.main_window_v_layout.setContentsMargins(0, 0, 0, 0)
        self.top_bar_h_layout = QHBoxLayout()
        self.top_bar_h_layout.setObjectName(u"top_bar_h_layout")
        self.horizontalSpacer = QSpacerItem(60, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.top_bar_h_layout.addItem(self.horizontalSpacer)

        self.jeff_pic = QLabel(self.verticalLayoutWidget)
        self.jeff_pic.setObjectName(u"jeff_pic")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.jeff_pic.sizePolicy().hasHeightForWidth())
        self.jeff_pic.setSizePolicy(sizePolicy1)
        self.jeff_pic.setBaseSize(QSize(100, 100))
        self.jeff_pic.setStyleSheet(u"image: url(:/newPrefix/JEFF.png);")

        self.top_bar_h_layout.addWidget(self.jeff_pic)

        self.horizontalSpacer_2 = QSpacerItem(60, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.top_bar_h_layout.addItem(self.horizontalSpacer_2)


        self.main_window_v_layout.addLayout(self.top_bar_h_layout)

        self.name_links_frame = QFrame(self.verticalLayoutWidget)
        self.name_links_frame.setObjectName(u"name_links_frame")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.name_links_frame.sizePolicy().hasHeightForWidth())
        self.name_links_frame.setSizePolicy(sizePolicy2)
        self.name_links_frame.setMinimumSize(QSize(100, 100))
        self.name_links_frame.setAutoFillBackground(False)
        self.name_links_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.name_links_frame.setFrameShadow(QFrame.Shadow.Plain)
        self.verticalLayoutWidget_2 = QWidget(self.name_links_frame)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(0, 0, 381, 102))
        self.app_info_v_layout = QVBoxLayout(self.verticalLayoutWidget_2)
        self.app_info_v_layout.setSpacing(0)
        self.app_info_v_layout.setObjectName(u"app_info_v_layout")
        self.app_info_v_layout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.app_info_v_layout.setContentsMargins(0, 0, 0, 0)
        self.app_name_label = QLabel(self.verticalLayoutWidget_2)
        self.app_name_label.setObjectName(u"app_name_label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.app_name_label.sizePolicy().hasHeightForWidth())
        self.app_name_label.setSizePolicy(sizePolicy3)
        font = QFont()
        font.setPointSize(13)
        font.setBold(True)
        self.app_name_label.setFont(font)
        self.app_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.app_name_label.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.app_info_v_layout.addWidget(self.app_name_label)

        self.links_h_layout = QHBoxLayout()
        self.links_h_layout.setObjectName(u"links_h_layout")
        self.links_h_layout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.github_label = QLabel(self.verticalLayoutWidget_2)
        self.github_label.setObjectName(u"github_label")
        self.github_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.links_h_layout.addWidget(self.github_label)

        self.youtube_label = QLabel(self.verticalLayoutWidget_2)
        self.youtube_label.setObjectName(u"youtube_label")
        self.youtube_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.links_h_layout.addWidget(self.youtube_label)

        self.discord_label = QLabel(self.verticalLayoutWidget_2)
        self.discord_label.setObjectName(u"discord_label")
        self.discord_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.links_h_layout.addWidget(self.discord_label)


        self.app_info_v_layout.addLayout(self.links_h_layout)


        self.main_window_v_layout.addWidget(self.name_links_frame)

        self.actions_v_layout = QVBoxLayout()
        self.actions_v_layout.setObjectName(u"actions_v_layout")
        self.dll_select_h_layout = QHBoxLayout()
        self.dll_select_h_layout.setObjectName(u"dll_select_h_layout")
        self.browse_dll_button = QPushButton(self.verticalLayoutWidget)
        self.browse_dll_button.setObjectName(u"browse_dll_button")

        self.dll_select_h_layout.addWidget(self.browse_dll_button)

        self.dll_name_label = QLabel(self.verticalLayoutWidget)
        self.dll_name_label.setObjectName(u"dll_name_label")
        self.dll_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.dll_select_h_layout.addWidget(self.dll_name_label)


        self.actions_v_layout.addLayout(self.dll_select_h_layout)

        self.ac_disable_h_layout = QHBoxLayout()
        self.ac_disable_h_layout.setObjectName(u"ac_disable_h_layout")
        self.disable_ac_button = QPushButton(self.verticalLayoutWidget)
        self.disable_ac_button.setObjectName(u"disable_ac_button")

        self.ac_disable_h_layout.addWidget(self.disable_ac_button)

        self.ac_status_label = QLabel(self.verticalLayoutWidget)
        self.ac_status_label.setObjectName(u"ac_status_label")
        self.ac_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.ac_disable_h_layout.addWidget(self.ac_status_label)


        self.actions_v_layout.addLayout(self.ac_disable_h_layout)


        self.main_window_v_layout.addLayout(self.actions_v_layout)

        self.verticalSpacer = QSpacerItem(20, 150, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.main_window_v_layout.addItem(self.verticalSpacer)

        self.inject_v_layout = QVBoxLayout()
        self.inject_v_layout.setObjectName(u"inject_v_layout")
        self.inject_dll_button = QPushButton(self.verticalLayoutWidget)
        self.inject_dll_button.setObjectName(u"inject_dll_button")
        self.inject_dll_button.setAutoDefault(False)

        self.inject_v_layout.addWidget(self.inject_dll_button)

        self.inject_status_label = QLabel(self.verticalLayoutWidget)
        self.inject_status_label.setObjectName(u"inject_status_label")
        self.inject_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.inject_v_layout.addWidget(self.inject_status_label)


        self.main_window_v_layout.addLayout(self.inject_v_layout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Jeff Injector", None))
        self.jeff_pic.setText("")
        self.app_name_label.setText(QCoreApplication.translate("MainWindow", u"Jeff Injector v1.0.0", None))
        self.github_label.setText(QCoreApplication.translate("MainWindow", u"Github", None))
        self.youtube_label.setText(QCoreApplication.translate("MainWindow", u"Youtube", None))
        self.discord_label.setText(QCoreApplication.translate("MainWindow", u"Discord", None))
        self.browse_dll_button.setText(QCoreApplication.translate("MainWindow", u"Browse DLL", None))
        self.dll_name_label.setText(QCoreApplication.translate("MainWindow", u"DLL Name", None))
        self.disable_ac_button.setText(QCoreApplication.translate("MainWindow", u"Disable AntiCheat", None))
        self.ac_status_label.setText(QCoreApplication.translate("MainWindow", u"AC Status", None))
        self.inject_dll_button.setText(QCoreApplication.translate("MainWindow", u"Inject", None))
        self.inject_status_label.setText("")
    # retranslateUi

