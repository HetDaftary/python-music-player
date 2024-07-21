from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from mp3.musicEventHandler import MusicEventHandler

class TopWidget(QTableWidget):
    def __init__(self, songs, parent):
        super().__init__()
        self.parent = parent
        self.databaseObject = None
        self.songs = songs

        self.songSelectedByUser=-1

        self.labelHeaderNames = ['title', 'artist', 'album', 'year', 'genre', 'comment']     
        self.labelNames = []

        self.setRowCount(len(self.songs))
        self.setColumnCount(len(self.labelHeaderNames))

        for song in self.songs:
            ## To implement logic to get data from database.
            self.labelNames.append(MusicEventHandler.getSongData(song))

        self.labels = []

        self.setHorizontalHeaderLabels(self.labelHeaderNames)

        for i in range(len(self.labelNames)):
            self.labels.append([])
            for j in range(len(self.labelNames[0])):
                self.setItem(i, j, QTableWidgetItem(self.labelNames[i][j]))

        self.resizeColumnsToContents()
        self.setSelectionBehavior(QTableWidget.SelectRows)

        self.cellClicked.connect(self.handleCellClicked)

    def refreshPage():
        pass

    def handleCellClicked(self, i, j):
        self.songSelectedByUser = i