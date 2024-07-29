from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QSizePolicy, QMenu, QAction
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDropEvent
from mp3.musicEventHandler import MusicEventHandler

class TopWidget(QTableWidget):
    def __init__(self, songs, parent):
        super().__init__()
        self.parent = parent
        self.songs = songs
        self.songSelectedByUser=-1
        self.labelHeaderNames = ['Title', 'Artist', 'Album', 'Year', 'Genre', 'Comment']     

        self.databaseObject = self.parent.databaseObject # MainWidget is the parent widget of TopWidget.
        # MainWidget has the databaseObject

        self.refreshPage(self.songs)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.cellClicked.connect(self.handleCellClicked)
        #self.itemDoubleClicked.connect(self.parent.playSelectedButtonAction)
        self.setAcceptDrops(True)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSelectionMode(QTableWidget.SingleSelection)

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
                toWrite = songDataFromDatabase[0]
            else:
                songDataFromFile = [x.capitalize() for x in MusicEventHandler.getSongData(song)]
                self.databaseObject.writeSongDataToTable(song, *songDataFromFile)
                self.labelNames.append(songDataFromFile)

        for i in range(len(self.labelNames)):
            for j in range(len(self.labelNames[0])):
                item = QTableWidgetItem(self.labelNames[i][j])
                self.setItem(i, j, item)
                if j != len(self.labelNames[i]) - 1: 
                    # Only allow comments to be editable
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)

        self.resizeColumnsToContents()

    def handleCellClicked(self, i, j):
        self.songSelectedByUser = i

    def dragEnterEvent(self, event: QDropEvent):
        if event.mimeData().hasText():
            filesGiven = event.mimeData().text().strip().split('\n')
            for file in filesGiven:
                file = file.rstrip('\r') 
                if file.startswith("file://") and file.endswith(".mp3"):
                    self.parent.addSongWithPath(file[7:]) # converting file url to normal file.
    
    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            filePath = url.toLocalFile()
            print(filePath)

    def contextMenuEvent(self, event):
        self.menuOnRightClick = QMenu(self)

        self.addSongAction = QAction("Add a song")
        self.deleteSongAction = QAction("Delete a song")

        self.menuOnRightClick.addAction(self.addSongAction)
        self.menuOnRightClick.addAction(self.deleteSongAction)
        
        self.addSongAction.triggered.connect(lambda _: self.parent.addSong())
        self.deleteSongAction.triggered.connect(lambda _: self.parent.deleteSong())

        self.menuOnRightClick.exec_(event.globalPos())