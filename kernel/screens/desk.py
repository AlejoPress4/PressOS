from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QStackedLayout
from PyQt5.QtCore import QTimer, QDateTime, Qt
from PyQt5.QtGui import QPixmap

class DesktopScreen(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		# Crear un QLabel para la imagen de fondo
		self.fondo = QLabel(self)
		pixmap = QPixmap('graphic_resources/backgrounds/Untitled.png')
		self.fondo.setPixmap(pixmap)
		self.fondo.setScaledContents(True)  # Escalar la imagen para que cubra todo el QLabel

		# Crear un layout apilado para superponer widgets
		self.stacked_layout = QStackedLayout(self)

		# Añadir el QLabel de fondo al layout apilado
		self.stacked_layout.addWidget(self.fondo)

		# Crear un widget contenedor para los otros widgets
		self.container = QWidget()
		self.stacked_layout.addWidget(self.container)

		# Estilos de color: fondo oscuro y tonos fríos
		self.container.setStyleSheet("""
			QLabel {
				color: #D3D7DF;  /* Color de texto */
				font-size: 24px;
			}
			QPushButton {
				background-color: #3B4A6B;
				border-radius: 8px;
				padding: 15px;
				margin: 5px;
			}
		""")

		# Barra lateral con botones de texto como marcadores de posición
		self.sidebar_layout = QVBoxLayout()
		self.sidebar_layout.setSpacing(10)

		# Crear botones (reemplazar íconos con texto por simplicidad)
		buttons = ["Carpeta", "Chat", "Navegador", "Correo", "Video/Música", "Buscar"]
		for text in buttons:
			btn = QPushButton(text)
			self.sidebar_layout.addWidget(btn)

		# Reloj
		self.clock_label = QLabel()
		self.update_clock()

		# Temporizador para actualizar el reloj
		self.timer = QTimer(self)
		self.timer.timeout.connect(self.update_clock)
		self.timer.start(1000)

		# Layout principal
		main_layout = QHBoxLayout(self.container)
		main_layout.addLayout(self.sidebar_layout)
		main_layout.addStretch()
		main_layout.addWidget(self.clock_label)

		self.setLayout(self.stacked_layout)

	def resizeEvent(self, event):
		# Ajustar el tamaño del QLabel de fondo al tamaño de la ventana
		self.fondo.resize(self.size())
		super().resizeEvent(event)

	def update_clock(self):
		try:
			current_time = QDateTime.currentDateTime()
			self.clock_label.setText(current_time.toString("HH:mm dd/MM/yyyy"))
		except Exception as e:
			self.clock_label.setText("Error al obtener la hora")