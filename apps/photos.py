import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QFileDialog, QLabel, QListWidget, QStackedWidget, QGridLayout, QScrollArea, 
                             QSlider, QComboBox, QLineEdit, QToolBar, QAction, QSplitter, QFrame, QProgressBar)
from PyQt5.QtGui import QPixmap, QIcon, QImage, QPainter, QColor
from PyQt5.QtCore import Qt, QUrl, QSize, QTimer, QThread, pyqtSignal
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PIL import Image, ImageEnhance, ImageFilter
import cv2

class ThumbnailWorker(QThread):
    thumbnailCreated = pyqtSignal(str, QPixmap)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        try:
            if self.file_path.lower().endswith(('.mp4', '.avi', '.mov')):
                cap = cv2.VideoCapture(self.file_path)
                ret, frame = cap.read()
                if ret:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    image = Image.fromarray(frame)
                    image.thumbnail((100, 100))
                    qimage = QImage(image.tobytes(), image.size[0], image.size[1], QImage.Format_RGB888)
                    pixmap = QPixmap.fromImage(qimage)
                    self.thumbnailCreated.emit(self.file_path, pixmap)
                cap.release()
            else:
                image = Image.open(self.file_path)
                image.thumbnail((100, 100))
                qimage = QImage(image.tobytes(), image.size[0], image.size[1], QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qimage)
                self.thumbnailCreated.emit(self.file_path, pixmap)
        except Exception as e:
            print(f"Error creating thumbnail for {self.file_path}: {str(e)}")

class ThumbnailWidget(QWidget):
    clicked = pyqtSignal(str)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.image_label = QLabel()
        self.image_label.setFixedSize(100, 100)
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        self.text_label = QLabel(os.path.basename(self.file_path))
        self.text_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.text_label)

        self.setLayout(layout)

    def setPixmap(self, pixmap):
        self.image_label.setPixmap(pixmap)

    def mousePressEvent(self, event):
        self.clicked.emit(self.file_path)

class AdvancedMediaViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Visualizador Avanzado de Fotos y Videos')
        self.setGeometry(100, 100, 1200, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)

        self.setup_toolbar()
        self.setup_main_content()
        self.setup_controls()
        self.setup_edit_controls()
        self.setup_progress_bar()
        self.setup_themes()

        self.current_file = None
        self.is_grid_view = False

    def setup_toolbar(self):
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        self.browse_action = QAction(QIcon.fromTheme("folder-open"), "Explorar", self)
        self.browse_action.triggered.connect(self.browse_files)
        self.toolbar.addAction(self.browse_action)

        self.toggle_view_action = QAction(QIcon.fromTheme("view-grid"), "Cambiar Vista", self)
        self.toggle_view_action.triggered.connect(self.toggle_view)
        self.toolbar.addAction(self.toggle_view_action)

        self.toggle_theme_action = QAction(QIcon.fromTheme("preferences-desktop-theme"), "Cambiar Tema", self)
        self.toggle_theme_action.triggered.connect(self.toggle_theme)
        self.toolbar.addAction(self.toggle_theme_action)

    def setup_main_content(self):
        self.content_splitter = QSplitter(Qt.Horizontal)
        self.main_layout.addWidget(self.content_splitter)

        self.left_panel = QStackedWidget()
        self.content_splitter.addWidget(self.left_panel)

        self.file_list = QListWidget()
        self.file_list.itemClicked.connect(self.on_file_click)
        self.left_panel.addWidget(self.file_list)

        self.grid_scroll_area = QScrollArea()
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_scroll_area.setWidget(self.grid_widget)
        self.grid_scroll_area.setWidgetResizable(True)
        self.left_panel.addWidget(self.grid_scroll_area)

        self.right_panel = QStackedWidget()
        self.content_splitter.addWidget(self.right_panel)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.right_panel.addWidget(self.image_label)

        self.video_widget = QVideoWidget()
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.video_widget)
        self.right_panel.addWidget(self.video_widget)

    def setup_controls(self):
        controls_layout = QHBoxLayout()

        self.play_button = QPushButton('Reproducir')
        self.play_button.clicked.connect(self.play_pause)
        controls_layout.addWidget(self.play_button)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.sliderMoved.connect(self.set_position)
        controls_layout.addWidget(self.slider)

        self.main_layout.addLayout(controls_layout)

    def setup_edit_controls(self):
        edit_layout = QHBoxLayout()

        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setRange(-100, 100)
        self.brightness_slider.setValue(0)
        self.brightness_slider.valueChanged.connect(self.adjust_brightness)
        edit_layout.addWidget(QLabel("Brillo:"))
        edit_layout.addWidget(self.brightness_slider)

        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setRange(-100, 100)
        self.contrast_slider.setValue(0)
        self.contrast_slider.valueChanged.connect(self.adjust_contrast)
        edit_layout.addWidget(QLabel("Contraste:"))
        edit_layout.addWidget(self.contrast_slider)

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Normal", "Blanco y Negro", "Sepia", "Blur"])
        self.filter_combo.currentIndexChanged.connect(self.apply_filter)
        edit_layout.addWidget(QLabel("Filtro:"))
        edit_layout.addWidget(self.filter_combo)

        self.main_layout.addLayout(edit_layout)

    def setup_progress_bar(self):
        self.progress_bar = QProgressBar()
        self.main_layout.addWidget(self.progress_bar)

    def setup_themes(self):
        self.light_theme = """
            QWidget {
                background-color: #f0f0f0;
                color: #333;
            }
            QPushButton {
                background-color: #fff;
                border: 1px solid #ddd;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #e6e6e6;
            }
            QListWidget, QScrollArea {
                background-color: #fff;
                border: 1px solid #ddd;
            }
            QSlider::groove:horizontal {
                border: 1px solid #bbb;
                background: white;
                height: 10px;
                border-radius: 4px;
            }
            QSlider::sub-page:horizontal {
                background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1,
                    stop: 0 #66e, stop: 1 #bbf);
                background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,
                    stop: 0 #bbf, stop: 1 #55f);
                border: 1px solid #777;
                height: 10px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #eee, stop:1 #ccc);
                border: 1px solid #777;
                width: 13px;
                margin-top: -2px;
                margin-bottom: -2px;
                border-radius: 4px;
            }
        """

        self.dark_theme = """
            QWidget {
                background-color: #2c3e50;
                color: #ecf0f1;
            }
            QPushButton {
                background-color: #34495e;
                border: 1px solid #2c3e50;
                padding: 5px;
                border-radius: 3px;
                color: #ecf0f1;
            }
            QPushButton:hover {
                background-color: #4a6b8a;
            }
            QListWidget, QScrollArea {
                background-color: #34495e;
                border: 1px solid #2c3e50;
                color: #ecf0f1;
            }
            QSlider::groove:horizontal {
                border: 1px solid #bbb;
                background: #34495e;
                height: 10px;
                border-radius: 4px;
            }
            QSlider::sub-page:horizontal {
                background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1,
                    stop: 0 #3498db, stop: 1 #2980b9);
                border: 1px solid #2c3e50;
                height: 10px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #ecf0f1, stop:1 #bdc3c7);
                border: 1px solid #2c3e50;
                width: 13px;
                margin-top: -2px;
                margin-bottom: -2px;
                border-radius: 4px;
            }
        """
        self.setStyleSheet(self.light_theme)
        self.current_theme = "light"

    def browse_files(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Images/Videos (*.png *.jpg *.jpeg *.gif *.bmp *.mp4 *.avi *.mov)")
        if file_dialog.exec_():
            file_paths = file_dialog.selectedFiles()
            self.load_files(file_paths)

    def load_files(self, file_paths):
        self.file_list.clear()
        self.grid_layout = QGridLayout(self.grid_widget)
        for file_path in file_paths:
            filename = os.path.basename(file_path)
            self.file_list.addItem(filename)
            thumbnail_widget = ThumbnailWidget(file_path)
            thumbnail_widget.clicked.connect(self.on_file_click)
            row = self.grid_layout.rowCount()
            col = self.grid_layout.columnCount()
            if col >= 4:
                row += 1
                col = 0
            self.grid_layout.addWidget(thumbnail_widget, row, col)
            
            worker = ThumbnailWorker(file_path)
            worker.thumbnailCreated.connect(self.update_thumbnail)
            worker.start()

    def update_thumbnail(self, file_path, pixmap):
        for i in range(self.grid_layout.count()):
            widget = self.grid_layout.itemAt(i).widget()
            if isinstance(widget, ThumbnailWidget) and widget.file_path == file_path:
                widget.setPixmap(pixmap)
                break

    def on_file_click(self, item):
        if isinstance(item, str):
            file_path = item
        else:
            file_path = os.path.join(os.path.dirname(self.file_list.item(0).text()), item.text())
        
        self.current_file = file_path
        self.load_file(file_path)

    def load_file(self, file_path):
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            pixmap = QPixmap(file_path)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.right_panel.setCurrentWidget(self.image_label)
        elif file_path.lower().endswith(('.mp4', '.avi', '.mov')):
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
            self.right_panel.setCurrentWidget(self.video_widget)
            
            self.play_button.setText('Reproducir')
            self.media_player.play()

    def play_pause(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
            self.play_button.setText('Reproducir')
        else:
            self.media_player.play()
            self.play_button.setText('Pausar')

    def set_position(self, position):
        self.media_player.setPosition(position)

    def adjust_brightness(self, value):
        if self.current_file and self.current_file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            image = Image.open(self.current_file)
            enhancer = ImageEnhance.Brightness(image)
            enhanced_image = enhancer.enhance(1 + value / 100)
            self.apply_image_changes(enhanced_image)

    def adjust_contrast(self, value):
        if self.current_file and self.current_file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            image = Image.open(self.current_file)
            enhancer = ImageEnhance.Contrast(image)
            enhanced_image = enhancer.enhance(1 + value / 100)
            self.apply_image_changes(enhanced_image)

    def apply_filter(self, index):
        if self.current_file and self.current_file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            image = Image.open(self.current_file)
            if index == 1:  # Blanco y Negro
                enhanced_image = image.convert('L')
            elif index == 2:  # Sepia
                enhanced_image = self.sepia_filter(image)
            elif index == 3:  # Blur
                enhanced_image = image.filter(ImageFilter.BLUR)
            else:
                enhanced_image = image
            self.apply_image_changes(enhanced_image)

    def sepia_filter(self, image):
        width, height = image.size
        pixels = image.load()
        for py in range(height):
            for px in range(width):
                r, g, b = image.getpixel((px, py))
                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                pixels[px, py] = (tr, tg, tb)
        return image

    def apply_image_changes(self, image):
        qimage = QImage(image.tobytes(), image.size[0], image.size[1], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def toggle_view(self):
        self.is_grid_view = not self.is_grid_view
        self.left_panel.setCurrentIndex(1 if self.is_grid_view else 0)

    def toggle_theme(self):
        if self.current_theme == "light":
            self.setStyleSheet(self.dark_theme)
            self.current_theme = "dark"
        else:
            self.setStyleSheet(self.light_theme)
            self.current_theme = "light"

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.current_file:
            self.load_file(self.current_file)

def main():
    app = QApplication(sys.argv)
    viewer = AdvancedMediaViewer()
    viewer.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()