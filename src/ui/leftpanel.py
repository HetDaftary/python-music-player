import os

from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QInputDialog
from PyQt5.QtCore import Qt

class LeftPanel(QTreeWidget):
    def __init__(self, parent=None):
        super(LeftPanel, self).__init__(parent)
        self.parent = parent
        self.setHeaderHidden(True)

        self.initLibrarySongs()
        self.initPlaylistSongs()

    def initLibrarySongs(self):
        self.libraryItem = QTreeWidgetItem(["Library"])
        self.addTopLevelItem(self.libraryItem)      

    def initPlaylistSongs(self):
        self.playlistItem = QTreeWidgetItem(["Playlist"])
        self.addTopLevelItem(self.playlistItem)

    def createPlaylist(self):
        playlistName, ok = QInputDialog.getText(self, "Add Playlist", "Enter playlist name:")
        if ok:
            self.playlistItem.addChild(QTreeWidgetItem([playlistName]))