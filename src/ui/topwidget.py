import os
import urllib.parse

from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QSizePolicy, QMenu, QAction, QHeaderView
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDropEvent
from mp3.musicEventHandler import MusicEventHandler

class TopWidget(QTableWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.songSelectedByUser=-1
        self.labelHeaderNames = ['Title', 'Artist', 'Album', 'Year', 'Genre', 'Comment']     

        self.databaseObject = self.parent.databaseObject # MainWidget is the parent widget of TopWidget.
        # MainWidget has the databaseObject

        self.addMusicPathToDatabase()

        self.refreshPage(self.databaseObject.getSongs("library"))
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.cellClicked.connect(self.handleCellClicked)
        #self.itemDoubleClicked.connect(self.parent.playSelectedButtonAction) # Double click event would trigger play selected.
        self.setAcceptDrops(True)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setWordWrap(True)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSelectionMode(QTableWidget.SingleSelection)

    def addMusicPathToDatabase(self):
        for file in os.listdir(self.parent.parent.MUSIC_PATH):
            songName = os.path.join(self.parent.parent.MUSIC_PATH, file)
            songDataFromDatabase = self.databaseObject.getSongData(songName)
            if file.endswith(".mp3") and songDataFromDatabase != None and len(songDataFromDatabase) == 0:
                self.databaseObject.writeSongDataToTable("library", songName, *MusicEventHandler.getSongData(songName))

    def refreshPage(self, songs):
        self.songs = songs
        
        self.clearContents()

        self.setRowCount(len(songs))
        self.setColumnCount(len(self.labelHeaderNames))

        self.labelNames = []

        self.setHorizontalHeaderLabels(self.labelHeaderNames)

        for song in songs:
            ## To implement logic to get data from database.
            songDataFromDatabase = self.databaseObject.getSongData(song)

            if len(songDataFromDatabase) != 0:
                self.labelNames.append([x.capitalize() for x in songDataFromDatabase[0]])

        for i in range(len(self.labelNames)):
            for j in range(len(self.labelNames[0])):
                item = QTableWidgetItem(self.labelNames[i][j])
                self.setItem(i, j, item)
                if j != len(self.labelNames[i]) - 1: 
                    # Only allow comments to be editable
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)

    def handleCellClicked(self, i, j):
        self.songSelectedByUser = i

    def dragEnterEvent(self, event: QDropEvent):
        if event.mimeData().hasText():
            filesGiven = event.mimeData().text().strip().split('\n')
            for file in filesGiven:
                file = file.rstrip('\r')
                file = urllib.parse.unquote(file)
                if file.startswith("file://") and file.endswith(".mp3"):
                    self.parent.addSongWithPath(file[7:]) # converting file url to normal file.
    
    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            filePath = url.toLocalFile()
            print(filePath)

    def contextMenuEvent(self, event):
        self.menuOnRightClick = QMenu(self)

        self.addSongAction = QAction(f"Add song to {self.parent.parent.selectedPlaylist}")
        self.addSongAction.triggered.connect(lambda _: self.parent.addSong())
        self.menuOnRightClick.addAction(self.addSongAction)

        if self.parent.parent.selectedPlaylist == "Library":
            self.addToPlaylistAction = QMenu("Add to playlist")

            self.actions = []

            for playlistName in self.parent.parent.leftPanel.getPlaylists():
                self.actions.append(QAction(playlistName))
                self.addToPlaylistAction.addAction(self.actions[-1])
                self.actions[-1].triggered.connect(lambda _: self.parent.addToPlaylist(playlistName))

            self.menuOnRightClick.addMenu(self.addToPlaylistAction)

        self.menuOnRightClick.addSeparator()
        
        self.deleteSongAction = QAction("Delete currently selected song")
        self.deleteSongAction.triggered.connect(lambda _: self.parent.deleteSong())
        self.menuOnRightClick.addAction(self.deleteSongAction)

        self.menuOnRightClick.exec_(event.globalPos())