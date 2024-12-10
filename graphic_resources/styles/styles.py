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
}

QPushButton#shutdown {
    qproperty-icon: url('./graphic_resources/icons/shutdown.png');
    qproperty-iconSize: 63px 63px;
    background: transparent;
}
QPushButton#reboot {
    qproperty-icon: url('./graphic_resources/icons/reboot.png');
    qproperty-iconSize: 64px 64px;
    background: transparent;
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
}


QPushButton#btn_apps {
    qproperty-icon: url('./graphic_resources/icons/btn_apps.png');
    background: transparent;
    qproperty-iconSize: 61px 51px;
}

QPushButton#shutdown {
    qproperty-icon: url('./graphic_resources/icons/shutdown.png');
    qproperty-iconSize: 61px 51px;
    background: transparent;
}
QPushButton#reboot {
    qproperty-icon: url('./graphic_resources/icons/reboot.png');
    qproperty-iconSize: 64px 64px;
    background: transparent;
}

QFrame#time_desk {
    background-color: rgba(0, 0, 0, 0.5);
    border-radius: 10px;
}

QFrame#time_desk QLabel {
    color: white;
    font-family: Arial, sans-serif;
    qproperty-alignment: AlignCenter;
}

QFrame#time_desk QLabel:first-child {
    font-size: 36px;
    font-weight: bold;
}

QFrame#time_desk QLabel:last-child {
    font-size: 18px;
}
"""
# Nuevo estilo para el asistente
assistantST = """
QWidget#centralwidget {
    background-color: #f0f0f0;
}

QTextEdit, QLineEdit {
    background-color: white;
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 5px;
    font-size: 14px;
}

QPushButton#send_button {
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 8px 16px;
    font-size: 14px;
}

QPushButton#send_button:hover {
    background-color: #45a049;
}
"""

# New style for the browser
browserST = """
QMainWindow {
    background-color: #f0f0f0;
}

QLineEdit {
    background-color: white;
    border: 1px solid #ddd;
    border-radius: 20px;
    padding: 5px 10px;
    font-size: 14px;
    margin: 5px;
}

QPushButton {
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 15px;
    padding: 5px 10px;
    font-size: 16px;
    margin: 5px;
}

QPushButton:hover {
    background-color: #45a049;
}

QWebEngineView {
    border: 1px solid #ddd;
    border-radius: 5px;
}
"""
def set_photo(photo_box, image_path):
    photo_label = QtWidgets.QLabel(photo_box)
    photo_label.setGeometry(photo_box.rect())
    photo_label.setPixmap(QPixmap(image_path).scaled(photo_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
    photo_label.setAlignment(Qt.AlignCenter)
    return photo_label
