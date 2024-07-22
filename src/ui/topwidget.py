from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from mp3.musicEventHandler import MusicEventHandler

class TopWidget(QTableWidget):
    def __init__(self, songs, parent):
        super().__init__()
        self.parent = parent
        self.songs = songs
        self.songSelectedByUser=-1
        self.labelHeaderNames = ['title', 'artist', 'album', 'year', 'genre', 'comment']     

        self.databaseObject = self.parent.databaseObject # MainWidget is the parent widget of TopWidget.
        # MainWidget has the databaseObject

        self.refreshPage()
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.cellClicked.connect(self.handleCellClicked)

    def refreshPage(self):
        self.clearContents()

        self.setRowCount(len(self.songs))
        self.setColumnCount(len(self.labelHeaderNames))

        self.labelNames = []

        for song in self.songs:
            ## To implement logic to get data from database.
            songDataFromDatabase = self.databaseObject.getSongData(song)

            if len(songDataFromDatabase) != 0:
                self.labelNames.append(songDataFromDatabase[0])
            else:
                songDataFromFile = MusicEventHandler.getSongData(song)
                self.databaseObject.writeSongDataToTable(song, *songDataFromFile)
                self.labelNames.append(songDataFromFile)

        self.setHorizontalHeaderLabels(self.labelHeaderNames)

        for song in self.songs:
            ## To implement logic to get data from database.
            self.labelNames.append(MusicEventHandler.getSongData(song))

        for i in range(len(self.labelNames)):
            for j in range(len(self.labelNames[0])):
                self.setItem(i, j, QTableWidgetItem(self.labelNames[i][j]))

        self.resizeColumnsToContents()

    def handleCellClicked(self, i, j):
        self.songSelectedByUser = i