import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QListWidget, QLabel, QSlider, QFileDialog, QStyle, QSizePolicy)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

class MusicPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.current_playlist = []
        self.current_track = 0

    def initUI(self):
        self.setWindowTitle('Reproductor de Música')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #f2f2f2;
                color: #333;
            }
            QPushButton {
                background-color: #fff;
                border: none;
                padding: 10px;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #e6e6e6;
            }
            QListWidget {
                background-color: #fff;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 8px;
                background: #ffffff;
                margin: 2px 0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #1db954;
                border: 1px solid #5c5c5c;
                width: 18px;
                margin: -2px 0;
                border-radius: 9px;
            }
        """)

        main_layout = QVBoxLayout()

        # Playlist
        self.playlist = QListWidget()
        self.playlist.itemDoubleClicked.connect(self.play_selected)
        main_layout.addWidget(self.playlist)

        # Now Playing
        now_playing_layout = QHBoxLayout()
        self.current_song_label = QLabel("No song playing")
        self.current_song_label.setAlignment(Qt.AlignCenter)
        self.current_song_label.setFont(QFont("Arial", 14, QFont.Bold))
        now_playing_layout.addWidget(self.current_song_label)
        main_layout.addLayout(now_playing_layout)

        # Progress Bar
        self.progress_slider = QSlider(Qt.Horizontal)
        self.progress_slider.sliderMoved.connect(self.set_position)
        main_layout.addWidget(self.progress_slider)

        # Control Buttons
        control_layout = QHBoxLayout()
        
        self.previous_button = QPushButton()
        self.previous_button.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipBackward))
        self.previous_button.clicked.connect(self.previous_track)
        
        self.play_pause_button = QPushButton()
        self.play_pause_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_pause_button.clicked.connect(self.play_pause)
        
        self.next_button = QPushButton()
        self.next_button.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
        self.next_button.clicked.connect(self.next_track)
        
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(70)
        self.volume_slider.setFixedWidth(100)
        self.volume_slider.valueChanged.connect(self.set_volume)

        control_layout.addWidget(self.previous_button)
        control_layout.addWidget(self.play_pause_button)
        control_layout.addWidget(self.next_button)
        control_layout.addWidget(self.volume_slider)
        
        main_layout.addLayout(control_layout)

        # Add Music Button
        add_music_button = QPushButton("Agregar Música")
        add_music_button.clicked.connect(self.add_music)
        main_layout.addWidget(add_music_button)

        self.setLayout(main_layout)

        # Media Player
        self.media_player = QMediaPlayer()
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)
        self.media_player.stateChanged.connect(self.state_changed)

    def add_music(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Seleccionar archivos de música", "", "Audio Files (*.mp3 *.wav *.ogg)")
        for file in files:
            self.playlist.addItem(os.path.basename(file))
            self.current_playlist.append(file)

    def play_selected(self):
        self.current_track = self.playlist.currentRow()
        self.play_music()

    def play_music(self):
        if self.current_playlist:
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.current_playlist[self.current_track])))
            self.media_player.play()
            self.current_song_label.setText(os.path.basename(self.current_playlist[self.current_track]))

    def play_pause(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
        else:
            self.play_music()

    def previous_track(self):
        if self.current_track > 0:
            self.current_track -= 1
            self.play_music()

    def next_track(self):
        if self.current_track < len(self.current_playlist) - 1:
            self.current_track += 1
            self.play_music()

    def set_position(self, position):
        self.media_player.setPosition(position)

    def position_changed(self, position):
        self.progress_slider.setValue(position)

    def duration_changed(self, duration):
        self.progress_slider.setRange(0, duration)

    def state_changed(self, state):
        if state == QMediaPlayer.PlayingState:
            self.play_pause_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.play_pause_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def set_volume(self, volume):
        self.media_player.setVolume(volume)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = MusicPlayer()
    player.show()
    sys.exit(app.exec_())