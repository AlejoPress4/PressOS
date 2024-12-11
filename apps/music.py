import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QListWidget, QLabel, QSlider, QFileDialog, 
                             QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QMessageBox)
from PyQt5.QtGui import QColor, QLinearGradient, QPainter, QBrush
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from kernel.modules.config.functions import press_os

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

class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Obtener el sistema y el usuario actual
        self.sistema = press_os()
        self.current_user = self.sistema.get_current_user()
        
        # Configurar la ventana
        self.setWindowTitle(f'Reproductor de Música - {self.current_user.username}')
        self.setGeometry(100, 100, 800, 600)

        # Configurar el directorio de música del usuario
        self.music_directory = os.path.join(self.current_user.get_user_path(), 'Musica')

        # Configurar widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Visualizer
        self.visualizer = VisualizerWidget()
        main_layout.addWidget(self.visualizer)

        # Now Playing
        self.current_song_label = QLabel("No hay canción reproduciendo")
        self.current_song_label.setAlignment(Qt.AlignCenter)
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

        # Cargar música inicial
        self.load_initial_music()

        # Timer for visualizer update
        self.visualizer_timer = QTimer(self)
        self.visualizer_timer.timeout.connect(self.update_visualizer)
        self.visualizer_timer.start(100)

    def load_initial_music(self):
        # Cargar todas las canciones del directorio de música del usuario
        supported_formats = ['.mp3', '.wav', '.ogg', '.flac']
        for filename in os.listdir(self.music_directory):
            if any(filename.lower().endswith(fmt) for fmt in supported_formats):
                file_path = os.path.join(self.music_directory, filename)
                self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
                self.playlist_widget.addItem(filename)

    def add_music(self):
        # Abrir diálogo para seleccionar archivos de música
        files, _ = QFileDialog.getOpenFileNames(
            self, 
            "Seleccionar archivos de música", 
            self.music_directory, 
            "Audio Files (*.mp3 *.wav *.ogg *.flac)"
        )
        
        for file in files:
            # Copiar archivos al directorio de música del usuario si no están ya ahí
            if os.path.dirname(file) != self.music_directory:
                import shutil
                shutil.copy(file, self.music_directory)
            
            filename = os.path.basename(file)
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(file)))
            self.playlist_widget.addItem(filename)

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
        self.progress_slider.setMaximum(duration)

    def set_volume(self, volume):
        self.media_player.setVolume(volume)

    def toggle_shuffle(self):
        # Alternar modo aleatorio
        current_mode = self.playlist.playbackMode()
        if current_mode == QMediaPlaylist.Sequential:
            self.playlist.setPlaybackMode(QMediaPlaylist.Random)
            self.shuffle_button.setText("🔀 (ON)")
        else:
            self.playlist.setPlaybackMode(QMediaPlaylist.Sequential)
            self.shuffle_button.setText("🔀")

    def state_changed(self, state):
        if state == QMediaPlayer.PlayingState:
            self.play_pause_button.setText("⏸")
            # Actualizar la etiqueta de la canción actual
            current_index = self.playlist.currentIndex()
            if current_index != -1:
                self.current_song_label.setText(
                    self.playlist_widget.item(current_index).text()
                )
        elif state == QMediaPlayer.PausedState:
            self.play_pause_button.setText("▶")
        elif state == QMediaPlayer.StoppedState:
            self.play_pause_button.setText("▶")

    def update_visualizer(self):
        # Simular visualización de audio
        current_volume = self.media_player.volume()
        self.visualizer.update_visualizer(current_volume)

    def handle_error(self, error):
        # Manejar errores de reproducción
        print(f"Error de reproducción: {error}")
        QMessageBox.warning(self, "Error de Reproducción", 
                             "No se pudo reproducir la canción.")

def main():
    app = QApplication(sys.argv)
    player = MusicPlayer()
    player.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()