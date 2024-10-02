import os, sys, PyQt5
from PyQt5.QtWidgets import QApplication, QMainWindow
from kernel.screens.desk1 import Ui_Desk_Window
from kernel.screens.login import Ui_Login_Window

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Sistema Operativo Simulado')
        self.showMaximized()
        self.show_desktop()

    def show_login(self):
        self.login_screen = Ui_Login_Window()
        self.login_screen.setupUi(self)
        #self.login_screen.login_button.clicked.connect(self.show_desktop)
        self.show()

    def show_desktop(self):
        # self.login_window.close()
        self.desktop_screen = Ui_Desk_Window()
        self.desktop_screen.setupUi(self)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = Main()
    sys.exit(app.exec_())