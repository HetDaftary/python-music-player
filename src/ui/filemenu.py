from PyQt5.QtWidgets import QMenu, QAction

class FileMenu(QMenu):
    def __init__(self, isMainMenu = True, parent = None):
        super().__init__("File", parent)
        self.parent = parent
        self.isMainMenu = isMainMenu

        self.openSongAction = QAction("Open and play a song")
        self.exitAppAction = QAction("Close")
        self.addSongAction = QAction("Add song to library")
        self.deleteSongAction = QAction("Delete currently selected song")

        self.addAction(self.openSongAction)
        self.addAction(self.exitAppAction)
        self.addSeparator()
        self.addAction(self.addSongAction)
        self.addAction(self.deleteSongAction)
        self.addSeparator()
        
        if self.isMainMenu:
            self.createPlaylistAction = QAction("Create a playlist")
            self.addAction(self.createPlaylistAction)
