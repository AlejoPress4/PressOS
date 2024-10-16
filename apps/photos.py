import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel, QListWidget
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget

class PhotoViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Visualizador de Fotos y Multimedia')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                color: #333;
            }
            QPushButton {
                background-color: #fff;
                border: 1px solid #ddd;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #e6e6e6;
            }
            QListWidget {
                background-color: #fff;
                border: 1px solid #ddd;
            }
        """)

        # Layout principal
        main_layout = QHBoxLayout()

        # Panel izquierdo para la lista de archivos
        left_panel = QVBoxLayout()
        self.file_list = QListWidget()
        self.file_list.itemClicked.connect(self.on_file_click)
        left_panel.addWidget(self.file_list)

        browse_button = QPushButton('Explorar')
        browse_button.clicked.connect(self.browse_folder)
        left_panel.addWidget(browse_button)

        # Panel derecho para la visualización
        right_panel = QVBoxLayout()
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        right_panel.addWidget(self.image_label)

        self.video_widget = QVideoWidget()
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.video_widget)
        right_panel.addWidget(self.video_widget)
        self.video_widget.hide()

        # Controles de reproducción
        controls_layout = QHBoxLayout()
        self.play_button = QPushButton('Reproducir')
        self.play_button.clicked.connect(self.play_pause)
        controls_layout.addWidget(self.play_button)
        right_panel.addLayout(controls_layout)

        # Agregar paneles al layout principal
        main_layout.addLayout(left_panel, 1)
        main_layout.addLayout(right_panel, 3)

        self.setLayout(main_layout)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta")
        if folder:
            self.load_files(folder)

    def load_files(self, folder):
        self.file_list.clear()
        for file in os.listdir(folder):
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.mp4', '.avi', '.mov')):
                self.file_list.addItem(file)

    def on_file_click(self, item):
        file_path = os.path.join(os.path.dirname(self.file_list.item(0).text()), item.text())
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            self.display_image(file_path)
        elif file_path.lower().endswith(('.mp4', '.avi', '.mov')):
            self.play_video(file_path)

    def display_image(self, file_path):
        self.video_widget.hide()
        self.image_label.show()
        pixmap = QPixmap(file_path)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def play_video(self, file_path):
        self.image_label.hide()
        self.video_widget.show()
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
        self.play_button.setText('Reproducir')
        self.media_player.play()

    def play_pause(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
            self.play_button.setText('Reproducir')
        else:
            self.media_player.play()
            self.play_button.setText('Pausar')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = PhotoViewer()
    viewer.show()
    sys.exit(app.exec_())