import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QTimer
from time import strftime

class DesktopScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Escritorio")
        self.setGeometry(0, 0, 1920, 1080)  # Ajusta el tamaño de la ventana según tu pantalla

        self.initUI()

    def initUI(self):
        # Crear un QLabel para la imagen de fondo
        self.background_label = QLabel(self)
        self.pixmap = QPixmap('graphic_resources/backgrounds/Untitled.png')  
        if self.pixmap.isNull():
            print("Error: No se pudo cargar la imagen de fondo.")
        self.background_label.setPixmap(self.pixmap)
        self.background_label.setScaledContents(True)
        self.background_label.setGeometry(0, 0, self.width(), self.height())

        # Crear un layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)  # Sin márgenes

        # Crear un layout para los íconos
        icon_layout = QVBoxLayout()
        icon_layout.setSpacing(10)  # Espaciado entre íconos

        app_icons = [
            ("Aplicación 1", "images/photo_3.jpg"),
            ("Aplicación 2", "images/photo_4.jpg"),
            ("Aplicación 3", "images/photo_5.jpg"),
            ("Aplicación 4", "images/photo_6.jpg"),
            ("Aplicación 5", "images/photo_7.jpg"),
            ("Aplicación 6", "images/photo_8.jpg"),
            ("Aplicación 7", "images/photo_9.jpg"),
            ("Aplicación 8", "images/photo_10.jpg"),
        ]

        for app_name, app_icon in app_icons:
            button = QPushButton()
            button.setIcon(QIcon(app_icon))
            button.setIconSize(QPixmap(app_icon).scaled(64, 64).size())  # Tamaño del ícono
            button.setStyleSheet("""
                background-color: rgba(31, 35, 51, 0.9);  /* Fondo de los íconos semi-transparente */
                border: none;
                border-radius: 10px;
                padding: 10px;
                text-align: left;
            """)
            button.setFixedSize(80, 80)  # Tamaño del botón para que sea cuadrado
            button.setToolTip(app_name)  # Tooltip con el nombre de la aplicación
            icon_layout.addWidget(button)

        # Crear un layout para la hora y la fecha
        time_frame = QFrame(self)
        time_frame.setStyleSheet("background-color: rgba(0, 0, 0, 0.7);")  # Fondo semi-transparente
        time_layout = QVBoxLayout()

        self.time_label = QLabel(self)
        self.time_label.setFont(QFont("Arial", 40))  # Tamaño de fuente ajustado
        self.time_label.setStyleSheet("color: white; padding: 10px;")
        self.time_label.setAlignment(Qt.AlignCenter)

        self.date_label = QLabel(self)
        self.date_label.setFont(QFont("Arial", 20))  # Tamaño de fuente ajustado
        self.date_label.setStyleSheet("color: white; margin: 5px 0;")  # Espacio reducido
        self.date_label.setAlignment(Qt.AlignCenter)  # Alinear al centro

        time_layout.addWidget(self.time_label)
        time_layout.addWidget(self.date_label)
        time_frame.setLayout(time_layout)

        # Crear un layout horizontal para organizar los íconos y la hora/fecha
        bottom_layout = QHBoxLayout()
        bottom_layout.addLayout(icon_layout)
        bottom_layout.addWidget(time_frame, alignment=Qt.AlignBottom | Qt.AlignRight)

        # Añadir el layout horizontal al layout principal
        main_layout.addLayout(bottom_layout)

        # Configuración de temporizador para actualizar hora y fecha
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        self.setLayout(main_layout)
        self.update_time()  # Mostrar la hora y fecha desde el inicio

    def resizeEvent(self, event):
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.background_label.setPixmap(self.pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

    def update_time(self):
        current_time = strftime("%H:%M:%S")
        current_date = strftime("%A, %d %B %Y")
        self.time_label.setText(current_time)
        self.date_label.setText(current_date)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    desktop = DesktopScreen()
    desktop.showFullScreen()  # Mostrar en pantalla completa
    desktop.setAttribute(Qt.WA_TranslucentBackground)  # Habilitar fondo translúcido
    desktop.show()
    sys.exit(app.exec_())

