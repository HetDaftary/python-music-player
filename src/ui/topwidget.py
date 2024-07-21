from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt5.QtCore import Qt
from mp3.musicEventHandler import MusicEventHandler

class TopWidget(QWidget):
    def __init__(self, songs, parent):
        super().__init__()
        self.parent = parent
        self.databaseObject = None

        self.songs = songs

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.layout.setAlignment(Qt.AlignTop) 
    
        self.labelNames = [['title', 'artist', 'album', 'year', 'genre']]

        for song in self.songs:
            ## To implement logic to get data from database.
            self.labelNames.append(MusicEventHandler.getSongData(song))

        self.labels = []

        for i in range(len(self.labelNames)):
            self.labels.append([])
            for j in range(len(self.labelNames[0])):
                self.labels[i].append(QLabel(self.labelNames[i][j]))
                self.layout.addWidget(self.labels[i][j], i, j)
                self.labels[i][j].setAlignment(Qt.AlignCenter)
        
    def refreshPage():
        pass