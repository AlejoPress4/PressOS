from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
class LoginScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        # Estilos de color: fondo oscuro y tonos fríos
        self.setStyleSheet("""
            QWidget {
                background-color: #1C1F2B;  /* Fondo oscuro */
            }
            QLabel {
                color: #D3D7DF;  /* Color de texto en tonos claros */
            }
            QLineEdit {
                background-color: #2C303C;
                color: #D3D7DF;
                border: 2px solid #3B3F51;
                padding: 10px;
                font-size: 16px;
                border-radius: 8px;
            }
            QPushButton {
                background-color: #3B4A6B;
                color: #D3D7DF;
                padding: 12px;
                font-size: 16px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #4A5B7C;
            }
        """)

        # Foto de la cuenta (Placeholder)
        self.photo_label = QLabel("Foto de la cuenta")
        self.photo_label.setAlignment(Qt.AlignCenter)
        self.photo_label.setFixedSize(200, 200)
        self.photo_label.setStyleSheet("border: 2px solid #3B3F51; border-radius: 10px;")

        # Campos de nombre de usuario y contraseña
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuario")
        self.username_input.setFixedWidth(300)
        self.username_input.setFont(QFont('Arial', 14))

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedWidth(300)
        self.password_input.setFont(QFont('Arial', 14))

        # Conectar la tecla Enter a la validación de login
        self.password_input.returnPressed.connect(self.validate_login)

        # Botón para iniciar sesión (debajo de los campos de usuario y contraseña)
        self.login_button = QPushButton("Iniciar Sesión")
        self.login_button.setFixedWidth(300)
        self.login_button.clicked.connect(self.validate_login)

        # Botón para cambiar cuenta
        self.change_account_button = QPushButton("Cambiar Cuenta")
        self.change_account_button.setFixedWidth(200)

        # Disposición de la foto y el botón de cambiar cuenta
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.photo_label)
        left_layout.addWidget(self.change_account_button)
        left_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # Disposición de los campos de texto (usuario, contraseña, y el botón de iniciar sesión)
        form_layout = QVBoxLayout()
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.login_button)
        form_layout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        # Layout principal que agrupa la imagen y el formulario
        main_layout = QHBoxLayout()
        main_layout.addStretch()
        main_layout.addLayout(left_layout)
        main_layout.addLayout(form_layout)
        main_layout.addStretch()

        # Botones de apagar y retorno en la parte inferior derecha
        self.shutdown_button = QPushButton()
        self.shutdown_button.setFixedSize(50, 50)
        self.shutdown_button.setStyleSheet("background: no-repeat center;")

        self.return_button = QPushButton()
        self.return_button.setFixedSize(50, 50)
        self.return_button.setStyleSheet("background: no-repeat center;")

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.shutdown_button)
        bottom_layout.addWidget(self.return_button)

        # Layout final que agrupa todo
        final_layout = QVBoxLayout()
        final_layout.addStretch()
        final_layout.addLayout(main_layout)
        final_layout.addStretch()
        final_layout.addLayout(bottom_layout)

        self.setLayout(final_layout)

    def validate_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Llamar a la función para verificar credenciales desde el archivo
        if self.check_credentials(username, password):
            self.main_window.show_desktop()  # Cambiar a la pantalla de escritorio
        else:
            self.show_error_message("Usuario o contraseña incorrectos.")

    def check_credentials(self, username, password):
        # Leer el archivo de credenciales
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    stored_username, stored_password = line.strip().split(',')
                    if username == stored_username and password == stored_password:
                        return True
        except FileNotFoundError:
            self.show_error_message("Archivo de usuarios no encontrado.")
            return False

        return False

    def show_error_message(self, message):
        error_dialog = QMessageBox()
        error_dialog.setWindowTitle("Error de inicio de sesión")
        error_dialog.setText(message)
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.exec_()

