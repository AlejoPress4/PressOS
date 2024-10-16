from PyQt5.QtCore import QPropertyAnimation, QRect, pyqtSignal
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore

def toggle_frames(frame1, frame2):
    frame1.hide()
    frame2.show()
    animate_bubble(frame2)

def animate_bubble(frame):
    animation = QPropertyAnimation(frame, b"geometry")
    animation.setDuration(500)
    animation.setStartValue(QRect(frame.x() + frame.width() // 2, frame.y() + frame.height() // 2, 0, 0))
    animation.setEndValue(QRect(frame.x(), frame.y(), frame.width(), frame.height()))
    animation.start()

def add_labels_to_layout(applications, layout, parent, open_application, is_grid=False):
	"""
	Agrega etiquetas (QLabel) a un layout dado.
	"""
	row, col = 0, 0
	for app in applications:
		label = ClickableLabel(parent)
		#label.setObjectName(f"icon_{app['name'].lower()}")  
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
    
class ClickableLabel(QLabel):
	clicked = pyqtSignal()

	def __init__(self, parent=None):
		super().__init__(parent)

	def mousePressEvent(self, event):
		self.clicked.emit()
		super().mousePressEvent(event)