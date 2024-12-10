from email.policy import default
import os, sys, PyQt5
from PyQt5.QtWidgets import QApplication, QMainWindow
from kernel.screens.desk1 import Ui_Desk_Window
from kernel.screens.login import Ui_Login_Window
from kernel.modules.config.functions import press_os
from PyQt5.QtCore import *

class Main(QMainWindow):
    config = press_os()
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Sistema Operativo Simulado')
        self.showFullScreen() 
        self.show_login()
        #self.show_desktop()

    def show_login(self):
        self.login_screen = Ui_Login_Window(self.config)
        self.login_screen.setupUi(self)
        #self.login_screen.pushButton.clicked.connect(self.handle_login) 
        self.login_screen.pass_lb.clicked.connect(lambda: self.show_desktop() if self.login_screen.login() else print("Nope"))
        self.show()
        
    # def handle_login(self):
    #     username = self.login_screen.username_input.text()
    #     password = self.login_screen.password_input.text()
    #     if self.login_screen.press_os_instance.login(username, password):
    #         self.show_desktop(self.login_screen.press_os_instance.get_current_user())
    #     else:
    #         self.login_screen.password_input.setText('')
    #         return False

        
    def show_desktop(self, usuario):
        self.login_screen.close()
        self.desktop_screen = Ui_Desk_Window()
        self.desktop_screen.setupUi(self)
        self.desktop_screen.usuario = usuario
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = Main()
    sys.exit(app.exec_())