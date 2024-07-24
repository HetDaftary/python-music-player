import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QSizePolicy
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDropEvent, QDragEnterEvent
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

class SongTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super(SongTableWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(['Title', 'Artist', 'Duration'])
        
        # Set size policy to expand
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        pass
    
    def dropEvent(self, event: QDropEvent):
        print(event.mimeData().text())
    
    def addSong(self, file_path):
        try:
            audio = MP3(file_path, ID3=EasyID3)
            title = audio.get('title', ['Unknown Title'])[0]
            artist = audio.get('artist', ['Unknown Artist'])[0]
            duration = int(audio.info.length)
            duration_str = f"{duration // 60}:{duration % 60:02d}"
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return
        
        row = self.rowCount()
        self.insertRow(row)
        self.setItem(row, 0, QTableWidgetItem(title))
        self.setItem(row, 1, QTableWidgetItem(artist))
        self.setItem(row, 2, QTableWidgetItem(duration_str))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Song List")
        self.setGeometry(100, 100, 600, 400)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        self.song_table = SongTableWidget()
        
        # Set stretch factor for the song table to take more space
        layout.addWidget(self.song_table)
        central_widget.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())