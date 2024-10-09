from PyQt5 import QtCore, QtGui, QtWidgets
import subprocess
from kernel.modules.config.functions_ui import toggle_frames, add_labels_to_layout, ClickableLabel
from graphic_resources.styles.styles import *
from kernel.modules.config.functions_ui import *
import cv2

class Ui_Desk_Window(object):
    def setupUi(self, Desk_Window):
        Desk_Window.setObjectName("Desk_Window")
        # Desk_Window.resize(1920, 1080)
        self.centralwidget = QtWidgets.QWidget(Desk_Window)
        self.centralwidget.setObjectName("centralwidget")
        apply_styles(Desk_Window, deskST)
        self.apps_bar = QtWidgets.QFrame(self.centralwidget)
        self.apps_bar.setGeometry(QtCore.QRect(0, 70, 120, 811))
        self.apps_bar.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.apps_bar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.apps_bar.setObjectName("apps_bar")
        
        # Usar un QVBoxLayout para apps_bar
        self.apps_bar_layout = QtWidgets.QVBoxLayout(self.apps_bar)
        self.apps_bar_layout.setGeometry(QtCore.QRect(0, 0, 120, 811))
        self.apps_bar_layout.setContentsMargins(15, 0, 0, 90)  # Dejar espacio en la parte inferior
        self.apps_bar.setLayout(self.apps_bar_layout)
        
        self.apps_window = QtWidgets.QFrame(self.centralwidget)
        self.apps_window.setGeometry(QtCore.QRect(160, 70, 1571, 781))
        self.apps_window.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.apps_window.setFrameShadow(QtWidgets.QFrame.Raised)
        self.apps_window.setObjectName("apps_window")
        # self.apps_window.hide()  # Ocultar inicialmente
        
        self.btn_apps = QtWidgets.QPushButton(self.apps_bar)
        self.btn_apps.setGeometry(QtCore.QRect(20, 720, 90, 90))
        self.btn_apps.setObjectName("btn_apps")
        
        # Usar un QGridLayout para apps_window
        self.apps_window_layout = QtWidgets.QGridLayout(self.apps_window)
        self.apps_window.setLayout(self.apps_window_layout)
        
        self.options_apps = QtWidgets.QFrame(self.apps_window)
        self.options_apps.setGeometry(QtCore.QRect(0, 709, 1571, 71))
        self.options_apps.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.options_apps.setFrameShadow(QtWidgets.QFrame.Raised)
        self.options_apps.setObjectName("options_apps")
        
        self.shutdown = QtWidgets.QPushButton(self.options_apps)
        self.shutdown.setGeometry(QtCore.QRect(1470, 10, 61, 51))
        self.shutdown.setText("")
        self.shutdown.setObjectName("shutdown")
        self.shutdown.clicked.connect(lambda: shutdown(self.desk_screen, self))
        
        self.user_lb = QtWidgets.QLabel(self.options_apps)
        self.user_lb.setGeometry(QtCore.QRect(40, 10, 501, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.user_lb.setFont(font)
        self.user_lb.setText("")
        self.user_lb.setObjectName("user_lb")
        
        self.reboot = QtWidgets.QPushButton(self.options_apps)
        self.reboot.setGeometry(QtCore.QRect(1380, 10, 61, 51))
        self.reboot.setText("")
        self.reboot.setObjectName("reboot")
        self.shutdown.clicked.connect(lambda: reboot(self.login_screen, self))
        
        self.asist_btn = QtWidgets.QPushButton(self.centralwidget)
        self.asist_btn.setGeometry(QtCore.QRect(940, 890, 91, 81))
        self.asist_btn.setText("")
        self.asist_btn.setObjectName("asist_btn")
        
        self.time_desk = QtWidgets.QFrame(self.centralwidget)
        self.time_desk.setGeometry(QtCore.QRect(1530, 850, 361, 121))
        self.time_desk.setAutoFillBackground(False)
        self.time_desk.setStyleSheet("")
        self.time_desk.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.time_desk.setFrameShadow(QtWidgets.QFrame.Raised)
        self.time_desk.setObjectName("time_desk")
        
        self.logo = QtWidgets.QFrame(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(1770, 10, 120, 80))
        self.logo.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.logo.setFrameShadow(QtWidgets.QFrame.Raised)
        self.logo.setObjectName("logo")

        # Lista de aplicaciones
        self.applications = [
            {"name": "Notepad", "command": ["notepad.exe"]},
            {"name": "Paint", "command": ["mspaint.exe"]},
            {"name" : "Music", "command": ["mediaplayer.exe"]},
            {"name": "Photos", "command": ["explorer.exe", "shell:AppsFolder\\Microsoft.Windows.Photos_8wekyb3d8bbwe!App"]},
            {"name": "Calculator", "command": ["calc.exe"]},
            # {"name": "", "command": [""]},
        ]

        # Agregar etiquetas a apps_bar
        add_labels_to_layout(self.applications, self.apps_bar_layout, self.apps_bar, self.open_application)

        # Agregar etiquetas a apps_window
        add_labels_to_layout(self.applications, self.apps_window_layout, self.apps_window, self.open_application, is_grid=True)

        # Conectar el botón para alternar la visibilidad de los frames
        self.btn_apps.clicked.connect(self.toggle_apps_window)

        Desk_Window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Desk_Window)
        self.statusbar.setObjectName("statusbar")
        Desk_Window.setStatusBar(self.statusbar)

        self.retranslateUi(Desk_Window)
        QtCore.QMetaObject.connectSlotsByName(Desk_Window)

    def retranslateUi(self, Desk_Window):
        _translate = QtCore.QCoreApplication.translate
        Desk_Window.setWindowTitle(_translate("Desk_Window", "MainWindow"))

    # Método para abrir aplicaciones nativas de Windows
    def open_application(self, command):
        subprocess.Popen(command)

    def toggle_apps_window(self):
        if self.apps_bar.isVisible():
            toggle_frames(self.apps_bar, self.apps_window)
        else:
            toggle_frames(self.apps_window, self.apps_bar)
            
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    sys.exit(app.exec_())
