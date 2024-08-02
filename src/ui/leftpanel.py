import os

from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QInputDialog, QMessageBox
from PyQt5.QtCore import Qt

class LeftPanel(QTreeWidget):
    def __init__(self, databaseObject, parent=None):
        super(LeftPanel, self).__init__(parent)
        self.parent = parent
        self.setHeaderHidden(True)

        self.initLibrarySongs()
        self.initPlaylistSongs()

    def initLibrarySongs(self):
        self.libraryItem = QTreeWidgetItem(["Library"])
        self.addTopLevelItem(self.libraryItem)      
        self.libraryItem.setSelected(True)

    def initPlaylistSongs(self):
        self.playlistItem = QTreeWidgetItem(["Playlist"])
        self.addTopLevelItem(self.playlistItem)

    def getPlaylists(self):
        return []

    def createPlaylist(self):
        playlistName, ok = QInputDialog.getText(self, "Add Playlist", "Enter playlist name:")
        if ok:
            self.playlistItem.addChild(QTreeWidgetItem([playlistName]))

            playlists = self.getPlaylists()

            if playlistName.lower() == "library" or playlistName in playlists:
                self.errorMessage = QMessageBox.critical(self, "Playlist name error", "Playlist name cannot be library or any existing playlist")
