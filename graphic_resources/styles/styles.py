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

QLabel#user_now {
    color: white;
}

QLabel#pass_lb {
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
    background: red;
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
    background-color: rgba(0, 0, 0, 0.3);  
    border-radius: 15px;  
    padding: 5px;  
}

QFrame#time_desk QLabel {
    color: white;
    font-family: 'Segoe UI', Arial, sans-serif;  
    qproperty-alignment: AlignCenter;
}

QFrame#time_desk QLabel:first-child {  
    font-size: 48px;  
    font-weight: bold;
    margin-bottom: 5px; 
}

QFrame#time_desk QLabel:last-child {  
    font-size: 24px; 
}

QPushButton#asist_btn {
    qproperty-icon: url('./graphic_resources/icons/assist.png');
    background: transparent;
    qproperty-iconSize: 91px 81px;
}
Qlabel#user_lb {
    color: white;
}


"""

def set_photo(photo_box, image_path):
    # Eliminar todos los widgets hijos de photo_box
    for child in photo_box.children():
        if isinstance(child, QtWidgets.QWidget):
            child.deleteLater()
    # Crear y configurar el QLabel para la nueva imagen
    photo_label = QtWidgets.QLabel(photo_box)
    photo_label.setGeometry(photo_box.rect())
    photo_label.setPixmap(QPixmap(image_path).scaled(photo_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
    photo_label.setAlignment(Qt.AlignCenter)
    photo_label.show()
