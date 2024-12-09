import re
from PyQt5 import QtCore, QtGui, QtWidgets
from kernel.modules.config.functions import press_os
from graphic_resources.styles.styles import *
from PyQt5.QtCore import pyqtSignal
from kernel.modules.config.functions_ui import *

class Ui_Login_Window(object):
    def setupUi(self, Main_Window):
        Main_Window.setObjectName("Login_Window")
        Main_Window.setMaximumSize(QtCore.QSize(16777215, 16777215))
        Main_Window.resize(1920, 1080)
        apply_styles(Main_Window, loginST)
        self.centralwidget = QtWidgets.QWidget(Main_Window)
        self.centralwidget.setObjectName("centralwidget")
        self.group_box = QtWidgets.QGroupBox(self.centralwidget)
        self.group_box.setGeometry(QtCore.QRect(270, 190, 1301, 651))
        self.group_box.setTitle("")
        self.group_box.setObjectName("group_box")

        # Botón para cambiar
        self.change_btn = QtWidgets.QPushButton(self.group_box)
        self.change_btn.setGeometry(QtCore.QRect(230, 510, 111, 31))
        self.change_btn.setObjectName("change_btn")

        # Botón de envío
        self.pushButton = QtWidgets.QPushButton(self.group_box)
        self.pushButton.setGeometry(QtCore.QRect(640, 390, 221, 28))
        self.pushButton.setObjectName("pushButton")

        # Entrada de contraseña
        self.pass_input = QtWidgets.QTextEdit(self.group_box)
        self.pass_input.setGeometry(QtCore.QRect(620, 340, 271, 31))
        self.pass_input.setObjectName("pass_input")

        # Marco de la foto
        self.photo_box = QtWidgets.QFrame(self.group_box)
        self.photo_box.setGeometry(QtCore.QRect(70, 80, 441, 411))
        self.photo_box.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.photo_box.setFrameShadow(QtWidgets.QFrame.Raised)
        self.photo_box.setObjectName("photo_box")

        # Configuración de la imagen
        set_photo(self.photo_box, "./graphic_resources/photoProfile/photo_profile.jpg")

        # Etiqueta de contraseña
        self.pass_lb = QtWidgets.QLabel(self.group_box)
        self.pass_lb.setGeometry(QtCore.QRect(620, 300, 221, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pass_lb.setFont(font)
        self.pass_lb.setObjectName("pass_lb")

        # Usuario actual
        self.user_now = QtWidgets.QLabel(self.group_box)
        self.user_now.setGeometry(QtCore.QRect(610, 140, 501, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.user_now.setFont(font)

        # Botones de apagado y reinicio
        self.shutdown = QtWidgets.QPushButton(self.centralwidget)
        self.shutdown.setGeometry(QtCore.QRect(1670, 900, 81, 71))
        self.shutdown.setText("")
        self.shutdown.setObjectName("shutdown")
        self.shutdown.clicked.connect(lambda: shutdown(self.login_screen, self))

        self.reboot = QtWidgets.QPushButton(self.centralwidget)
        self.reboot.setGeometry(QtCore.QRect(1780, 900, 71, 71))
        self.reboot.setText("")
        self.reboot.setObjectName("reboot")
        self.shutdown.clicked.connect(lambda: reboot(self.login_screen, self))

        # Marco de la hora
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

    # def retranslateUi(self, Main_Window):
    #     _translate = QtCore.QCoreApplication.translate
    #     Main_Window.setWindowTitle(_translate("Login_Window", "Press OS"))
    #     self.change_btn.setText(_translate("Login_Window", "Change User"))
    #     self.pushButton.setText(_translate("Login_Window", "Press"))
    #     self.pass_lb.setText(_translate("Login_Window", "Password:"))
    #     self.user_now.setText(_translate("Login_Window", users['def_usr']))
    
    def retranslateUi(self, Main_Window):
        _translate = QtCore.QCoreApplication.translate
        Main_Window.setWindowTitle(_translate("Main_Window", "Main_Window"))
    def update_current_user_label(self):
        current_user = self.press_os_instance.get_current_user()
        self.user_now.setText(f"Current User: {current_user.username}")

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if self.press_os_instance.login(username, password):
            self.update_current_user_label()
            return True
        else:
            self.password_input.setText('')
            return False

    def change_user(self):
        self.user_combo.clear()
        usuarios = self.press_os_instance.obtener_usuarios()
        for usuario in usuarios:
            self.user_combo.addItem(usuario.username)
        self.user_combo.show()
        self.user_combo.activated[str].connect(self.user_selected)

    def user_selected(self, username):
        self.user_now.setText(f"Current User: {username}")
        self.user_combo.hide()
        self.press_os_instance.current_user = next(user for user in self.press_os_instance.obtener_usuarios() if user.username == username)


    # def login(self):
    #     password = self.pass_input.toPlainText()
    #     if press_os().login(password):
    #         # send to desktop
    #         return True
    #     else:
    #         self.pass_input.setText('')
    #         return False
    
    # def close(self):
    #     self.close() 