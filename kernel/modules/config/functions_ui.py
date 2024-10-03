from PyQt5.QtCore import QPropertyAnimation, QRect, pyqtSignal
from PyQt5.QtWidgets import QLabel
from PyQt5 import QtCore

def toggle_frames(frame1, frame2, show_window):
	"""
	Alterna la visibilidad de los frames apps_bar_layout y apps_window con animación.
	"""
	if show_window:
		frame1.hide()
		frame2.show()
		animate_bubble(frame2)
	else:
		frame2.hide()
		frame1.show()
        

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
		label.setObjectName(f"lbl_{app['name'].lower()}")
		label.setText(app["name"])
		label.setAlignment(QtCore.Qt.AlignCenter)
		label.setStyleSheet("border: 1px solid black; padding: 5px;")
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

class ClickableLabel(QLabel):
	clicked = pyqtSignal()

	def __init__(self, parent=None):
		super().__init__(parent)

	def mousePressEvent(self, event):
		self.clicked.emit()
		super().mousePressEvent(event)
