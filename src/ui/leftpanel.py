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

        self.itemSelectionChanged.connect(self.onItemSelected)
        self.itemDoubleClicked.connect(self.onItemDoubleClicked)

    def onItemSelected(self):
        pass

    def onItemDoubleClicked(self):
        selectedItem = self.currentItem()
        if selectedItem:
            # Do something with the selected item
            itemText = selectedItem.text(0).lower()
            if itemText != "playlist":
                self.parent.mainWidget.selectedPlaylist = itemText
                print(self.parent.mainWidget.selectedPlaylist)
                self.parent.mainWidget.refreshTopWidget()

    def initLibrarySongs(self):
        self.libraryItem = QTreeWidgetItem(["Library"])
        self.addTopLevelItem(self.libraryItem)      
        self.libraryItem.setSelected(True)

    def initPlaylistSongs(self):
        self.playlistItem = QTreeWidgetItem(["Playlist"])
        self.addTopLevelItem(self.playlistItem)

        playlistsToAdd = self.parent.mainWidget.databaseObject.getPlaylists()

        for playlistName in playlistsToAdd:
            if playlistName != "library":
                item = QTreeWidgetItem([playlistName])
                self.playlistItem.addChild(item)

    def getPlaylists(self):
        return set([self.playlistItem.child(i).text(0).capitalize() for i in range(self.playlistItem.childCount())])

    def createPlaylist(self):
        playlistName, ok = QInputDialog.getText(self, "Add Playlist", "Enter playlist name:")
        if ok:
            playlists = self.getPlaylists()

            if playlistName.lower() != "library" and playlistName not in playlists:
                self.playlistItem.addChild(QTreeWidgetItem([playlistName]))
            else:
                self.errorMessage = QMessageBox.critical(self, "Playlist name error", "Playlist name cannot be library or any existing playlist")

        self.parent.mainWidget.databaseObject.addPlaylist(playlistName)
        self.parent.mainWidget.refreshTopWidget()
