from PyQt5.QtWidgets import QMenu, QAction

class FileMenu(QMenu):
    def __init__(self, title, parent = None):
        super().__init__(title, parent)
        self.parent = parent
        
        self.openSongAction = QAction("Open and play a song")
        self.exitAppAction = QAction("Close")
        self.addSongAction = QAction("Add song to library")
        self.deleteSongAction = QAction("Delete currently selected song")
        self.createPlaylistAction = QAction("Create a playlist")

        self.addAction(self.openSongAction)
        self.addAction(self.exitAppAction)
        self.addSeparator()
        self.addAction(self.addSongAction)
        self.addAction(self.deleteSongAction)
        self.addSeparator()
        self.addAction(self.createPlaylistAction)

        self.openSongAction.triggered.connect(self.parent.mainWidget.openAndPlayAMp3)
        self.exitAppAction.triggered.connect(self.parent.closeAppMenuAction)
        self.addSongAction.triggered.connect(self.parent.mainWidget.addSong)
        self.deleteSongAction.triggered.connect(self.parent.mainWidget.deleteSong)
        self.createPlaylistAction.triggered.connect(self.parent.leftPanel.createPlaylist)

