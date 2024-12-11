from PyQt5 import QtCore, QtGui, QtWidgets
import subprocess, cv2
from kernel.modules.config.functions_ui import *
from graphic_resources.styles.styles import *
from kernel.modules.config.functions_ui import *
from kernel.modules.config.functions import *
from apps import *

class Ui_Desk_Window(object):
    def __init__(self, config: press_os):
        self.config = config
        
    def setupUi(self, Desk_Window):
        Desk_Window.setObjectName("Desk_Window")
        # Desk_Window.resize(1920, 1080)
        self.centralwidget = QtWidgets.QWidget(Desk_Window)
        self.centralwidget.setObjectName("centralwidget")
        apply_styles(Desk_Window, deskST)
        self.apps_bar = QtWidgets.QFrame(self.centralwidget)
        self.apps_bar.setGeometry(QtCore.QRect(0, 70, 120, 816))
        self.apps_bar.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.apps_bar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.apps_bar.setObjectName("apps_bar")
        
        #RGBBB pa
        self.timer = QTimer(self.apps_bar)
        self.timer.timeout.connect(lambda: actualizar_color_borde(self.apps_bar))
        self.timer.start(20)  # Actualiza cada 50ms
        
        # Usar un QVBoxLayout para apps_bar
        self.apps_bar_layout = QtWidgets.QVBoxLayout(self.apps_bar)
        self.apps_bar_layout.setGeometry(QtCore.QRect(0, 0, 120, 811))
        self.apps_bar_layout.setContentsMargins(0, 0, 0, 90)  # Dejar espacio en la parte inferior
        # self.apps_bar.setLayout(self.apps_bar_layout)
        
        self.apps_window = QtWidgets.QFrame(self.centralwidget)
        self.apps_window.setGeometry(QtCore.QRect(160, 70, 1571, 781))
        self.apps_window.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.apps_window.setFrameShadow(QtWidgets.QFrame.Raised)
        self.apps_window.setObjectName("apps_window")
        self.apps_window.hide()  # Ocultar inicialmente
        
        # RGBBB para apps_window
        self.timer_window = QTimer(self.apps_window)
        self.timer_window.timeout.connect(lambda: actualizar_color_borde(self.apps_window))
        self.timer_window.start(20)  # Actualiza cada 20ms
        
        # Usar un QGridLayout para apps_window
        self.apps_window_layout = QtWidgets.QGridLayout(self.apps_window)
        self.apps_window_layout.setContentsMargins(5, 15, 5, 90)  # Dejar espacio en la parte inferior
        
           
        self.btn_apps = QtWidgets.QPushButton(self.apps_bar)
        self.btn_apps.setGeometry(QtCore.QRect(20, 720, 90, 90))
        self.btn_apps.setObjectName("btn_apps")
    
        
        self.options_apps = QtWidgets.QFrame(self.apps_window)
        self.options_apps.setGeometry(QtCore.QRect(0, 709, 1571, 71))
        self.options_apps.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.options_apps.setFrameShadow(QtWidgets.QFrame.Raised)
        self.options_apps.setObjectName("options_apps")
        
        self.shutdown = QtWidgets.QPushButton(self.options_apps)
        self.shutdown.setGeometry(QtCore.QRect(1470, 10, 61, 51))
        self.shutdown.setObjectName("shutdown")
        self.shutdown.clicked.connect(lambda: shutdown())
        
        self.user_lb = QtWidgets.QLabel(self.options_apps)
        self.user_lb.setGeometry(QtCore.QRect(40, 10, 501, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.user_lb.setFont(font)
        self.user_lb.setText(f"{self.config.current_user.username}")
        self.user_lb.setStyleSheet("color: white;")
        self.user_lb.setObjectName("user_lb")
        
        self.reboot = QtWidgets.QPushButton(self.options_apps)
        self.reboot.setGeometry(QtCore.QRect(1380, 10, 61, 51))
        self.reboot.setObjectName("reboot")
        self.reboot.clicked.connect(lambda: reboot(Desk_Window))
        
        self.asist_btn = QtWidgets.QPushButton(self.centralwidget)
        self.asist_btn.setGeometry(QtCore.QRect(940, 890, 91, 81))
        self.asist_btn.setObjectName("asist_btn")
        self.asist_btn.clicked.connect(open_assistant)


        self.time_desk = QtWidgets.QFrame(self.centralwidget)
        self.time_desk.setGeometry(QtCore.QRect(1530, 850, 361, 121))
        self.time_desk.setAutoFillBackground(False)
        self.time_desk.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.time_desk.setFrameShadow(QtWidgets.QFrame.Raised)
        self.time_desk.setObjectName("time_desk")
        
        # Crear labels para mostrar la hora y la fecha
        self.time_label = QtWidgets.QLabel(self.time_desk)
        self.date_label = QtWidgets.QLabel(self.time_desk)

        # Usar un QVBoxLayout para time_desk
        layout = QtWidgets.QVBoxLayout(self.time_desk)
        layout.addWidget(self.time_label)
        layout.addWidget(self.date_label)

        # Configurar las propiedades de los labels
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: update_time(self.time_label, self.date_label))
        self.timer.start(1000)  # Update every second

        # Initial update
        update_time(self.time_label, self.date_label)

        
        self.logo = QtWidgets.QFrame(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(1770, 10, 120, 180))
        self.logo.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.logo.setFrameShadow(QtWidgets.QFrame.Raised)
        self.logo.setObjectName("logo")

        # Lista de aplicaciones
        self.applications = [
            {"name": "Calculator", "command": ["python" , "./apps/calculator.py"], "icon": "./graphic_resources/icons/calculator.png"},
            {"name": "Photos", "command": ["python" , "./apps/photos.py"] , "icon": "./graphic_resources/icons/photos.png"},
            {"name" : "Music", "command": ["python" , "./apps/music.py"], "icon": "./graphic_resources/icons/music.png"},
            {"name": "Task Manager", "command": ["python" , "./apps/task.py"], "icon": "./graphic_resources/icons/task.png"},
            {"name": "Browser", "command": ["python", "./apps/browser.py"], "icon": "./graphic_resources/icons/Otter_Browser.png"},
            {"name": "Files", "command": ["python", "./apps/files.py"], "icon": "./graphic_resources/icons/folder.png"},
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
        print("Toggle apps window")
        print(self.apps_bar.isVisible())
        if self.apps_bar.isVisible():
            toggle_frames(self.apps_bar, self.apps_window)
        else:
            toggle_frames(self.apps_window, self.apps_bar)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    sys.exit(app.exec_())
