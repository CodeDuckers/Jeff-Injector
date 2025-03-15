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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QHBoxLayout,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QStatusBar, QVBoxLayout, QWidget)
# import UI.jeff_profile_rc as jeff_profile_rc

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
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(60, 20, 281, 541))
        self.main_v_layout = QVBoxLayout(self.layoutWidget)
        self.main_v_layout.setSpacing(30)
        self.main_v_layout.setObjectName(u"main_v_layout")
        self.main_v_layout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.jeff_image = QLabel(self.layoutWidget)
        self.jeff_image.setObjectName(u"jeff_image")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.jeff_image.sizePolicy().hasHeightForWidth())
        self.jeff_image.setSizePolicy(sizePolicy1)
        self.jeff_image.setBaseSize(QSize(100, 100))
        self.jeff_image.setTextFormat(Qt.TextFormat.AutoText)
        self.jeff_image.setPixmap(QPixmap(u":/newPrefix/JEFF_smaller.png"))
        self.jeff_image.setScaledContents(False)
        self.jeff_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.jeff_image.setWordWrap(False)

        self.verticalLayout_2.addWidget(self.jeff_image)

        self.app_title_label = QLabel(self.layoutWidget)
        self.app_title_label.setObjectName(u"app_title_label")
        font = QFont()
        font.setPointSize(19)
        font.setBold(True)
        self.app_title_label.setFont(font)
        self.app_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.app_title_label)


        self.main_v_layout.addLayout(self.verticalLayout_2)

        self.links_h_layout = QHBoxLayout()
        self.links_h_layout.setObjectName(u"links_h_layout")
        self.github_link_label = QLabel(self.layoutWidget)
        self.github_link_label.setObjectName(u"github_link_label")
        self.github_link_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.links_h_layout.addWidget(self.github_link_label)

        self.youtube_link_label = QLabel(self.layoutWidget)
        self.youtube_link_label.setObjectName(u"youtube_link_label")
        self.youtube_link_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.links_h_layout.addWidget(self.youtube_link_label)

        self.discord_link_label = QLabel(self.layoutWidget)
        self.discord_link_label.setObjectName(u"discord_link_label")
        self.discord_link_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.links_h_layout.addWidget(self.discord_link_label)


        self.main_v_layout.addLayout(self.links_h_layout)

        self.options_f_layout = QFormLayout()
        self.options_f_layout.setObjectName(u"options_f_layout")
        self.select_dll_label = QLabel(self.layoutWidget)
        self.select_dll_label.setObjectName(u"select_dll_label")

        self.options_f_layout.setWidget(0, QFormLayout.LabelRole, self.select_dll_label)

        self.select_dll_button = QPushButton(self.layoutWidget)
        self.select_dll_button.setObjectName(u"select_dll_button")

        self.options_f_layout.setWidget(0, QFormLayout.FieldRole, self.select_dll_button)

        self.injection_method_label = QLabel(self.layoutWidget)
        self.injection_method_label.setObjectName(u"injection_method_label")

        self.options_f_layout.setWidget(1, QFormLayout.LabelRole, self.injection_method_label)

        self.injection_method_select = QComboBox(self.layoutWidget)
        self.injection_method_select.addItem("")
        self.injection_method_select.setObjectName(u"injection_method_select")

        self.options_f_layout.setWidget(1, QFormLayout.FieldRole, self.injection_method_select)

        self.ac_status_label = QLabel(self.layoutWidget)
        self.ac_status_label.setObjectName(u"ac_status_label")

        self.options_f_layout.setWidget(2, QFormLayout.LabelRole, self.ac_status_label)

        self.ac_status_button = QPushButton(self.layoutWidget)
        self.ac_status_button.setObjectName(u"ac_status_button")

        self.options_f_layout.setWidget(2, QFormLayout.FieldRole, self.ac_status_button)


        self.main_v_layout.addLayout(self.options_f_layout)

        self.inject_v_layout = QVBoxLayout()
        self.inject_v_layout.setObjectName(u"inject_v_layout")
        self.inject_dll_button = QPushButton(self.layoutWidget)
        self.inject_dll_button.setObjectName(u"inject_dll_button")

        self.inject_v_layout.addWidget(self.inject_dll_button)

        self.inject_status_label = QLabel(self.layoutWidget)
        self.inject_status_label.setObjectName(u"inject_status_label")
        self.inject_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.inject_v_layout.addWidget(self.inject_status_label)


        self.main_v_layout.addLayout(self.inject_v_layout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Jeff Injector", None))
        self.jeff_image.setText("")
        self.app_title_label.setText(QCoreApplication.translate("MainWindow", u"Jeff Injector v1.0.0", None))
        self.github_link_label.setText(QCoreApplication.translate("MainWindow", u"Github", None))
        self.youtube_link_label.setText(QCoreApplication.translate("MainWindow", u"Youtube", None))
        self.discord_link_label.setText(QCoreApplication.translate("MainWindow", u"Discord", None))
        self.select_dll_label.setText(QCoreApplication.translate("MainWindow", u"Select DLL", None))
        self.select_dll_button.setText(QCoreApplication.translate("MainWindow", u"Select", None))
        self.injection_method_label.setText(QCoreApplication.translate("MainWindow", u"Injection Method", None))
        self.injection_method_select.setItemText(0, QCoreApplication.translate("MainWindow", u"LoadLibraryA", None))

        self.ac_status_label.setText(QCoreApplication.translate("MainWindow", u"Anticheat Status", None))
        self.ac_status_button.setText(QCoreApplication.translate("MainWindow", u"Enabled", None))
        self.inject_dll_button.setText(QCoreApplication.translate("MainWindow", u"Inject", None))
        self.inject_status_label.setText(QCoreApplication.translate("MainWindow", u"Injection Status", None))
    # retranslateUi

