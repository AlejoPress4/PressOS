import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QFileDialog, QMessageBox, QGridLayout, QCheckBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from kernel.modules.config.functions import press_os
from kernel.modules import Usuario
from kernel.modules.config import users

class UserCreationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.press_os = press_os()
        self.initUI()
        

    def initUI(self):
        self.setWindowTitle('Crear Nuevo Usuario')
        self.setGeometry(300, 300, 400, 300)

        layout = QGridLayout()

        # Username
        layout.addWidget(QLabel('Nombre de usuario:'), 0, 0)
        self.username_input = QLineEdit()
        layout.addWidget(self.username_input, 0, 1)

        # Password
        layout.addWidget(QLabel('Contraseña:'), 1, 0)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input, 1, 1)

        # Permissions
        layout.addWidget(QLabel('Permisos:'), 2, 0)
        self.admin_check = QCheckBox('Admin')
        self.read_check = QCheckBox('Read')
        self.write_check = QCheckBox('Write')
        layout.addWidget(self.admin_check, 2, 1)
        layout.addWidget(self.read_check, 3, 1)
        layout.addWidget(self.write_check, 4, 1)

        # Photo
        self.photo_path = None
        self.photo_button = QPushButton('Seleccionar Foto')
        self.photo_button.clicked.connect(self.select_photo)
        layout.addWidget(self.photo_button, 5, 0, 1, 2)

        # Create user button
        self.create_button = QPushButton('Crear Usuario')
        self.create_button.clicked.connect(self.create_user)
        layout.addWidget(self.create_button, 6, 0, 1, 2)

        self.setLayout(layout)

    def select_photo(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Seleccionar Foto', '', 'Image Files (*.png *.jpg *.bmp)')
        if file_name:
            self.photo_path = file_name
            self.photo_button.setText('Foto seleccionada')

    def create_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        permisos = []
        if self.admin_check.isChecked():
            permisos.append('admin')
        if self.read_check.isChecked():
            permisos.append('read')
        if self.write_check.isChecked():
            permisos.append('write')

        if not username or not password or not permisos:
            QMessageBox.warning(self, 'Error', 'Por favor, complete todos los campos obligatorios.')
            return

        if self.press_os.agregar_usuario(username, password, permisos, self.photo_path):
            QMessageBox.information(self, 'Éxito', f'Usuario {username} creado exitosamente.')
            self.clear_fields()
        else:
            QMessageBox.warning(self, 'Error', f'El usuario {username} ya existe.')

    def clear_fields(self):
        self.username_input.clear()
        self.password_input.clear()
        self.admin_check.setChecked(False)
        self.read_check.setChecked(False)
        self.write_check.setChecked(False)
        self.photo_path = None
        self.photo_button.setText('Seleccionar Foto')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UserCreationWindow()
    ex.show()
    sys.exit(app.exec_())