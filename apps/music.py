import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QListWidget, QLabel, QSlider, QFileDialog, 
                             QGraphicsView, QGraphicsScene, QGraphicsEllipseItem)
from PyQt5.QtGui import QIcon, QColor, QLinearGradient, QPainter, QPen, QBrush
from PyQt5.QtCore import Qt, QUrl, QTimer, QPointF
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist

class VisualizerWidget(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setStyleSheet("background: transparent;")
        self.bars = []
        self.create_bars()

    def create_bars(self):
        for i in range(20):
            bar = QGraphicsEllipseItem(0, 0, 10, 10)
            gradient = QLinearGradient(0, 0, 0, 10)
            gradient.setColorAt(0, QColor("#8E2DE2"))
            gradient.setColorAt(1, QColor("#4A00E0"))
            bar.setBrush(QBrush(gradient))
            self.scene.addItem(bar)
            self.bars.append(bar)

    def update_visualizer(self, value):
        for i, bar in enumerate(self.bars):
            height = (i + 1) * value / 5
            bar.setRect(i * 15, 100 - height, 10, height)

class AdvancedMusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Reproductor de Música Avanzado')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #1E1E1E;
                color: #FFFFFF;
            }
            QPushButton {
                background-color: #4A00E0;
                color: #FFFFFF;
                border: none;
                padding: 10px;
                margin: 5px;
                border-radius: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6C14FF;
            }
            QListWidget {
                background-color: #2D2D2D;
                color: #FFFFFF;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QSlider::groove:horizontal {
                border: 1px solid #4A00E0;
                height: 8px;
                background: #2D2D2D;
                margin: 2px 0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #8E2DE2;
                border: 1px solid #4A00E0;
                width: 18px;
                margin: -2px 0;
                border-radius: 9px;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Visualizer
        self.visualizer = VisualizerWidget()
        main_layout.addWidget(self.visualizer)

        # Now Playing
        self.current_song_label = QLabel("No hay canción reproduciendo")
        self.current_song_label.setAlignment(Qt.AlignCenter)
        self.current_song_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #8E2DE2;")
        main_layout.addWidget(self.current_song_label)

        # Progress Bar
        self.progress_slider = QSlider(Qt.Horizontal)
        self.progress_slider.sliderMoved.connect(self.set_position)
        main_layout.addWidget(self.progress_slider)

        # Control Buttons
        control_layout = QHBoxLayout()
        
        self.previous_button = QPushButton("⏮")
        self.previous_button.clicked.connect(self.previous_track)
        
        self.play_pause_button = QPushButton("▶")
        self.play_pause_button.clicked.connect(self.play_pause)
        
        self.next_button = QPushButton("⏭")
        self.next_button.clicked.connect(self.next_track)
        
        self.shuffle_button = QPushButton("🔀")
        self.shuffle_button.clicked.connect(self.toggle_shuffle)
        
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(70)
        self.volume_slider.setFixedWidth(100)
        self.volume_slider.valueChanged.connect(self.set_volume)

        control_layout.addWidget(self.previous_button)
        control_layout.addWidget(self.play_pause_button)
        control_layout.addWidget(self.next_button)
        control_layout.addWidget(self.shuffle_button)
        control_layout.addWidget(self.volume_slider)
        
        main_layout.addLayout(control_layout)

        # Playlist
        self.playlist_widget = QListWidget()
        self.playlist_widget.itemDoubleClicked.connect(self.play_selected)
        main_layout.addWidget(self.playlist_widget)

        # Add Music Button
        add_music_button = QPushButton("Agregar Música")
        add_music_button.clicked.connect(self.add_music)
        main_layout.addWidget(add_music_button)

        # Media Player
        self.playlist = QMediaPlaylist()
        self.media_player = QMediaPlayer()
        self.media_player.setPlaylist(self.playlist)
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)
        self.media_player.stateChanged.connect(self.state_changed)
        self.media_player.error.connect(self.handle_error)

        # Timer for visualizer update
        self.visualizer_timer = QTimer(self)
        self.visualizer_timer.timeout.connect(self.update_visualizer)
        self.visualizer_timer.start(100)

    def add_music(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Seleccionar archivos de música", "", "Audio Files (*.mp3 *.wav *.ogg)")
        for file in files:
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(file)))
            self.playlist_widget.addItem(os.path.basename(file))

    def play_selected(self):
        self.playlist.setCurrentIndex(self.playlist_widget.currentRow())
        self.media_player.play()

    def play_pause(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()

    def previous_track(self):
        self.playlist.previous()

    def next_track(self):
        self.playlist.next()

    def set_position(self, position):
        self.media_player.setPosition(position)

    def position_changed(self, position):
        self.progress_slider.setValue(position)

    def duration_changed(self, duration):
        self.progress_slider.setRange(0, duration)

    def state_changed(self, state):
        if state == QMediaPlayer.PlayingState:
            self.play_pause_button.setText("⏸")
            self.current_song_label.setText(self.playlist_widget.currentItem().text())
        else:
            self.play_pause_button.setText("▶")

    def set_volume(self, volume):
        self.media_player.setVolume(volume)

    def toggle_shuffle(self):
        if self.playlist.playbackMode() == QMediaPlaylist.Sequential:
            self.playlist.setPlaybackMode(QMediaPlaylist.Random)
            self.shuffle_button.setStyleSheet("background-color: #8E2DE2;")
        else:
            self.playlist.setPlaybackMode(QMediaPlaylist.Sequential)
            self.shuffle_button.setStyleSheet("")

    def update_visualizer(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            value = self.media_player.position() / self.media_player.duration() * 100
            self.visualizer.update_visualizer(value)

    def handle_error(self):
        error_message = self.media_player.errorString()
        self.current_song_label.setText(f"Error: {error_message}")
        print(f"Error: {error_message}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = AdvancedMusicPlayer()
    player.show()
    sys.exit(app.exec_())