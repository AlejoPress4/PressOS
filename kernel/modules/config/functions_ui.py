from PyQt5.QtCore import QPropertyAnimation, QRect, pyqtSignal, QTimer, QEasingCurve
from PyQt5.QtWidgets import QLabel, QGraphicsOpacityEffect
from PyQt5.QtGui import QPixmap, QColor
from PyQt5 import QtCore
import math, time
def toggle_frames(frame1, frame2):
    frame1.hide()
    frame2.show()
    animate_bubble(frame2, 100)

def animate_bubble(frame, duration):
    # Create opacity effect
    opacity_effect = QGraphicsOpacityEffect(frame)
    frame.setGraphicsEffect(opacity_effect)

    # Geometry animation
    geo_anim = QPropertyAnimation(frame, b"geometry")
    geo_anim.setDuration(duration)
    geo_anim.setStartValue(QRect(frame.x() + frame.width() // 2, frame.y() + frame.height() // 2, 0, 0))
    geo_anim.setEndValue(frame.geometry())
    geo_anim.setEasingCurve(QEasingCurve.OutBack)

    # Opacity animation
    opacity_anim = QPropertyAnimation(opacity_effect, b"opacity")
    opacity_anim.setDuration(duration)
    opacity_anim.setStartValue(0)
    opacity_anim.setEndValue(1)
    opacity_anim.setEasingCurve(QEasingCurve.InQuad)

    # Start animations
    geo_anim.start()
    opacity_anim.start()

    # Keep reference to animations to prevent garbage collection
    frame.geo_anim = geo_anim
    frame.opacity_anim = opacity_anim

def add_labels_to_layout(applications, layout, parent, open_application, is_grid=False):
	"""
	Agrega etiquetas (QLabel) a un layout dado.
	"""
	row, col = 0, 0
	for app in applications:
		label = ClickableLabel(parent)
		label.setObjectName(f"icon_{app['name'].lower()}")  
		label.setAlignment(QtCore.Qt.AlignCenter)
  
		icon_path = app["icon"]
		pixmap = QPixmap(icon_path)
  
		#Cargar el pixmap en la etiqueta
		if pixmap.isNull():
			print(f"Error: La imagen en la ruta {icon_path} no se pudo cargar.")
		else:
			pixmap = pixmap.scaled(81, 81, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
			label.setPixmap(pixmap)
		
		# label.setFixedSize(85, 85)
		label.command = app["command"]
		label.clicked.connect(lambda cmd=app["command"]: open_application(cmd))
		if is_grid:
			layout.addWidget(label, row, col)
			col += 1
			if col > 5:  
				col = 0
				row += 1
		else:
			layout.addWidget(label)

def shutdown(self):
    self.login_screen.close()
    self.desktop_screen.close()

def reboot(self):
    self.login_screen.refresh()
    self.desktop_screen.refresh()
    
def open_asist(self):
    self.asist_window.show()
    
start_time = time.time()
def actualizar_color_borde(frame):
    # Calcular el tiempo transcurrido desde el inicio
    current_time = (time.time() - start_time) * 1000  # Convertir a milisegundos

    # Calcular los valores RGB utilizando funciones sinusoidales
    red = int((math.sin(current_time * 0.002) + 1) * 127.5)
    green = int((math.sin(current_time * 0.002 + 2 * math.pi / 3) + 1) * 127.5)
    blue = int((math.sin(current_time * 0.002 + 4 * math.pi / 3) + 1) * 127.5)

    # Aplicar el estilo al frame
    frame.setStyleSheet(f"""
        QFrame#apps_bar {{
            border: 2px solid rgb({red}, {green}, {blue});
        }}
    """)
        
class ClickableLabel(QLabel):
	clicked = pyqtSignal()

	def __init__(self, parent=None):
		super().__init__(parent)

	def mousePressEvent(self, event):
		self.clicked.emit()
		super().mousePressEvent(event)