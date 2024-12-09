from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_users_window(object):
    def setupUi(self, users_window):
        users_window.setObjectName("users_window")
        users_window.resize(1902, 867)
        self.centralwidget = QtWidgets.QWidget(users_window)
        self.centralwidget.setObjectName("centralwidget")
        self.frame_usr = QtWidgets.QFrame(self.centralwidget)
        self.frame_usr.setGeometry(QtCore.QRect(290, 70, 1361, 591))
        self.frame_usr.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_usr.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_usr.setObjectName("frame_usr")
        self.delete_usr = QtWidgets.QPushButton(self.centralwidget)
        self.delete_usr.setGeometry(QtCore.QRect(1740, 700, 81, 81))
        self.delete_usr.setText("")
        self.delete_usr.setObjectName("delete_usr")
        self.logo = QtWidgets.QFrame(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(50, 30, 171, 80))
        self.logo.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.logo.setFrameShadow(QtWidgets.QFrame.Raised)
        self.logo.setObjectName("logo")
        users_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(users_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1902, 26))
        self.menubar.setObjectName("menubar")
        users_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(users_window)
        self.statusbar.setObjectName("statusbar")
        users_window.setStatusBar(self.statusbar)

        self.retranslateUi(users_window)
        QtCore.QMetaObject.connectSlotsByName(users_window)

    def retranslateUi(self, users_window):
        _translate = QtCore.QCoreApplication.translate
        users_window.setWindowTitle(_translate("users_window", "MainWindow"))
