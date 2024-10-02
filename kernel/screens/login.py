import re
from PyQt5 import QtCore, QtGui, QtWidgets
from kernel.modules.functions import press_os
from kernel.secrets import users

class Ui_Login_Window(object):
    def setupUi(self, Main_Window):
        Main_Window.setObjectName("Login_Window")
        # Main_Window.resize(1920, 1008)
        Main_Window.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralwidget = QtWidgets.QWidget(Main_Window)
        self.centralwidget.setObjectName("centralwidget")
        self.group_box = QtWidgets.QGroupBox(self.centralwidget)
        self.group_box.setGeometry(QtCore.QRect(270, 190, 1301, 651))
        self.group_box.setTitle("")
        self.group_box.setObjectName("group_box")
        self.change_btn = QtWidgets.QPushButton(self.group_box)
        self.change_btn.setEnabled(True)
        self.change_btn.setGeometry(QtCore.QRect(230, 510, 111, 31))
        self.change_btn.setObjectName("change_btn")
        self.pushButton = QtWidgets.QPushButton(self.group_box)
        self.pushButton.setGeometry(QtCore.QRect(640, 390, 221, 28))
        self.pushButton.setObjectName("pushButton")
        self.pass_input = QtWidgets.QTextEdit(self.group_box)
        self.pass_input.setGeometry(QtCore.QRect(620, 340, 271, 31))
        self.pass_input.setObjectName("pass_input")
        self.photo_box = QtWidgets.QFrame(self.group_box)
        self.photo_box.setGeometry(QtCore.QRect(70, 80, 441, 411))
        self.photo_box.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.photo_box.setFrameShadow(QtWidgets.QFrame.Raised)
        self.photo_box.setObjectName("photo_box")
        self.pass_lb = QtWidgets.QLabel(self.group_box)
        self.pass_lb.setGeometry(QtCore.QRect(620, 300, 221, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pass_lb.setFont(font)
        self.pass_lb.setObjectName("pass_lb")
        self.user_now = QtWidgets.QLabel(self.group_box)
        self.user_now.setGeometry(QtCore.QRect(610, 140, 501, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.user_now.setFont(font)
        self.user_now.setObjectName("user_now")
        self.shutdown = QtWidgets.QPushButton(self.centralwidget)
        self.shutdown.setGeometry(QtCore.QRect(1670, 900, 71, 61))
        self.shutdown.setText("")
        self.shutdown.setObjectName("shutdown")
        self.reboot = QtWidgets.QPushButton(self.centralwidget)
        self.reboot.setGeometry(QtCore.QRect(1780, 900, 71, 61))
        self.reboot.setText("")
        self.reboot.setObjectName("reboot")
        self.time_frame = QtWidgets.QFrame(self.centralwidget)
        self.time_frame.setGeometry(QtCore.QRect(1550, 40, 281, 111))
        self.time_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.time_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.time_frame.setObjectName("time_frame")
        Main_Window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Main_Window)
        self.statusbar.setObjectName("statusbar")
        Main_Window.setStatusBar(self.statusbar)

        self.retranslateUi(Main_Window)
        QtCore.QMetaObject.connectSlotsByName(Main_Window)

    def retranslateUi(self, Main_Window):
        _translate = QtCore.QCoreApplication.translate
        Main_Window.setWindowTitle(_translate("Main_Window", "MainWindow"))
        self.change_btn.setText(_translate("Main_Window", "Change User"))
        self.pushButton.setText(_translate("Main_Window", "Press"))
        self.pass_lb.setText(_translate("Main_Window", "Password"))
        self.user_now.setText(_translate("Main_Window", users['def_usr']))

    def close(self):
        self.centralwidget.close()


    def login(self):
        password = self.pass_input.toPlainText()        
        if press_os().login(password):
            # send to desktop
            return True
        else:
            self.pass_input.setText('')
            return False

        
        
        