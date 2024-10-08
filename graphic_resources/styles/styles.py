from PyQt5.QtGui import QPalette, QColor, QPixmap 
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets

def apply_styles(object, style):
    object.setStyleSheet(style)

loginST = """
QWidget#centralwidget {
    background-image: url('./graphic_resources/backgrounds/loginBG.jpg');
    background-repeat: no-repeat;
    background-position: center;
    background-size: cover;
}

QPushButton#shutdown {
    qproperty-icon: url('./graphic_resources/icons/shutdown.svg');
    qproperty-iconSize: 61px 61px;
    background: transparent;
    color: white;
}
QPushButton#reboot {
    qproperty-icon: url('./graphic_resources/icons/reboot.svg');
    qproperty-iconSize: 64px 64px;
    background: transparent;
    color: white;
}

QFrame#photo_box {
    border: 1px solid #ccc;
}

QGroupBox#group_box, QFrame#photo_box {
    border: none; 
    background: transparent; 
    border-radius: 10px;
}

QLabel#user_now, QLabel#pass_lb {
    color: white;
}

"""

deskST = """ 
QWidget#centralwidget {
    background-image: url('./graphic_resources/backgrounds/deskBG.jpg');
    background-repeat: no-repeat;
    background-position: center;
    background-size: cover;
}
QFrame#apps_bar {
border: 2px solid #FF5733;  # Cambia el color del borde aquí
}

QLabel#Calculator {
    qproperty-pixmap: url('./graphic_resources/icons/calculator.png');
    background: transparent;
}

QLabel#Notepad {
    qproperty-pixmap: url('./graphic_resources/icons/notepad.png');
    background: transparent;
}

QLabel#Camera{
    qproperty-pixmap: url('./graphic_resources/icons/notepad.png);
    background: transparent;
}

QLabel#Photos{
    qproperty-pixmap: url('./graphic_resources/icons/notepad.png');
    background: transparent;
}

QLabel#Paint {
    qproperty-pixmap: url('./graphic_resources/icons/paint.png');
    background: transparent;
}

"""
def set_photo(photo_box, image_path):
    photo_label = QtWidgets.QLabel(photo_box)
    photo_label.setGeometry(photo_box.rect())
    photo_label.setPixmap(QPixmap(image_path).scaled(photo_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
    photo_label.setAlignment(Qt.AlignCenter)
    return photo_label
