import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt6.QtCore import QUrl

import os

class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the media player
        self.player = QMediaPlayer()

        # Load an MP3 file
        url = QUrl.fromLocalFile(os.path.join(os.environ["PWD"], "data/mp3-files/14 Dangerous.mp3"))  # Replace with the path to your MP3 file
        content = QMediaContent(url)
        self.player.setMedia(content)

        # Create the UI
        self.initUI()

    def initUI(self):
        # Create buttons for play, pause, and stop
        playButton = QPushButton("Play", self)
        pauseButton = QPushButton("Pause", self)
        stopButton = QPushButton("Stop", self)

        # Connect buttons to their respective functions
        playButton.clicked.connect(self.play_music)
        pauseButton.clicked.connect(self.pause_music)
        stopButton.clicked.connect(self.stop_music)

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(playButton)
        layout.addWidget(pauseButton)
        layout.addWidget(stopButton)

        # Set up the main window
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setWindowTitle("PyQt6 MP3 Player")
        self.setGeometry(300, 300, 300, 150)

    def play_music(self):
        self.player.play()

    def pause_music(self):
        self.player.pause()

    def stop_music(self):
        self.player.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = MusicPlayer()
    player.show()
    sys.exit(app.exec_())