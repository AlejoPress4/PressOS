import sys
import os
import PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from kernel.screens.login import LoginScreen
from kernel.screens.desk import DesktopScreen

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.login_screen = LoginScreen(self)  
        self.desktop_screen = DesktopScreen()  
        self.setCentralWidget(self.login_screen)  
        self.setWindowTitle('Sistema Operativo Simulado') 
        self.showMaximized() 

    def show_desktop(self):
        self.setCentralWidget(self.desktop_screen)  

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)  
        main_window = Main() 
        sys.exit(app.exec_())  
    except Exception as e:
        print(f"An error occurred: {e}")