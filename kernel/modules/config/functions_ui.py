from PyQt5.QtCore import QPropertyAnimation, QRect, pyqtSignal, QTime, QDate, QTimer, QEasingCurve
from PyQt5.QtWidgets import QLabel, QGraphicsOpacityEffect, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QColor
from PyQt5 import QtCore
from kernel.modules.config.functions import press_os
import math, time
import sys
import os
from PyQt5.QtWidgets import QApplication
import subprocess

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
    
def update_time(time_label, date_label):
    current_time = QTime.currentTime()
    current_date = QDate.currentDate()
    
    time_text = current_time.toString('hh:mm:ss')
    date_text = current_date.toString('dddd, MMMM d, yyyy')
    
    time_label.setText(time_text)
    date_label.setText(date_text)


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
        QFrame {{
            border: 2px solid rgb({red}, {green}, {blue});
        }}
    """)

def agregar_usuarios_a_frame(frame, on_user_selected):
    # Limpiar el frame antes de agregar nuevos widgets
    for i in reversed(range(frame.layout().count())): 
        widget_to_remove = frame.layout().itemAt(i).widget()
        frame.layout().removeWidget(widget_to_remove)
        widget_to_remove.setParent(None)

    # Crear un layout vertical para el frame
    layout = QVBoxLayout(frame)
    frame.setLayout(layout)

    # Agregar cada usuario al layout
    for usuario in press_os.usuarios.values():
        # Crear un layout horizontal para cada usuario
        user_layout = QHBoxLayout()

        # Crear una QLabel para la foto de perfil
        foto_label = ClickableLabel()
        foto_label.username = usuario.username
        foto_label.clicked.connect(on_user_selected)
        pixmap = QPixmap(usuario.photo)
        foto_label.setPixmap(pixmap.scaled(50, 50, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))

        # Crear una QLabel para el nombre de usuario
        nombre_label = QLabel(usuario.username)

        # Agregar las QLabel al layout horizontal
        user_layout.addWidget(foto_label)
        user_layout.addWidget(nombre_label)

        # Agregar el layout horizontal al layout vertical
        layout.addLayout(user_layout)

    # Ajustar el layout del frame
    frame.setLayout(layout)
        
class ClickableLabel(QLabel):
	clicked = pyqtSignal()

	def __init__(self, parent=None):
		super().__init__(parent)

	def mousePressEvent(self, event):
		self.clicked.emit()
		super().mousePressEvent(event)

def shutdown():
    QApplication.quit()

def reboot(window: QWidget):
    window.close()
    python = sys.executable
    os.execl(python, python, *sys.argv)
    
def open_assistant():
    subprocess.Popen(["python", "./apps/assistant.py"])