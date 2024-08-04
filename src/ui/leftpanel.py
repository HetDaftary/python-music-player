import os

from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QInputDialog, QMessageBox, QMenu, QAction
from PyQt5.QtCore import Qt

class LeftPanel(QTreeWidget):
    def __init__(self, databaseObject, parent=None):
        super(LeftPanel, self).__init__(parent)
        self.parent = parent
        self.setHeaderHidden(True)

        self.currentlySelectedPlaylist = "Library"

        self.initLibrarySongs()
        self.initPlaylistSongs()

        self.itemSelectionChanged.connect(self.onItemSelected)
        self.itemDoubleClicked.connect(self.onItemDoubleClicked)

    def onItemSelected(self):
        selectedItem = self.currentItem()
        if selectedItem:
            # Do something with the selected item
            self.currentlySelectedPlaylist = selectedItem.text(0).capitalize()

    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)

        openInNewWindowAction = QAction('Open in New Window', self)
        #openInNewWindowAction.triggered.connect(lambda: self.action_triggered('Action 1'))
        contextMenu.addAction(openInNewWindowAction)

        contextMenu.addSeparator()

        deletePlaylistAction = QAction('Delete Playlist', self)
        deletePlaylistAction.triggered.connect(self.deletePlaylist)
        contextMenu.addAction(deletePlaylistAction)

        contextMenu.exec_(event.globalPos())

    def deletePlaylist(self):
        playlistWidget = self.currentItem()
        if playlistWidget:
            playlistName = self.currentlySelectedPlaylist
            playlistName = playlistName.capitalize()
            if playlistName != "Library" and playlistName != "Playlist":
                buttonPressed = QMessageBox.warning(self, "Confirm to delete playlist", f"Do you want to delete playlist: {playlistName}?", QMessageBox.Yes | QMessageBox.No)
                if buttonPressed == QMessageBox.Yes:
                    self.libraryItem.setSelected(True)
                    self.parent.mainWidget.databaseObject.deletePlaylist(playlistName)

                    index = self.indexOfTopLevelItem(playlistWidget)
                    if index != -1:
                        self.takeTopLevelItem(index)
                    else:
                        parent = playlistWidget.parent()
                        if parent:
                            parent.takeChild(parent.indexOfChild(playlistWidget))
            else:
                buttonPressed = QMessageBox.critical(self, "Cannot delete playlist", "Cannot delete library or playlist options")

        if self.currentlySelectedPlaylist == self.parent.mainWidget.selectedPlaylist:
            self.parent.mainWidget.selectedPlaylist = "Library"
            self.parent.mainWidget.refreshTopWidget()

    def onItemDoubleClicked(self):
        # Do something with the selected item
        itemText = self.currentlySelectedPlaylist
        if itemText != "playlist":
            self.parent.mainWidget.selectedPlaylist = itemText
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
        playlistName = playlistName.capitalize()
        if ok:
            playlists = self.getPlaylists()

            playlistName = playlistName.capitalize()
            if playlistName != "Library" and playlistName != "Playlist" and playlistName not in playlists:
                self.playlistItem.addChild(QTreeWidgetItem([playlistName]))
                self.parent.mainWidget.selectedPlaylist = playlistName
                self.parent.mainWidget.databaseObject.addPlaylist(playlistName)
                self.parent.mainWidget.refreshTopWidget()
            else:
                self.errorMessage = QMessageBox.critical(self, "Playlist name error", "Playlist name cannot be library, playlist or any existing playlist")
        
