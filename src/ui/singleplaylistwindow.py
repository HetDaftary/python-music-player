from PyQt5.QtWidgets import QMenuBar

from ui.mainwindow import MainWidget
from ui.filemenu import FileMenu
from ui.controlmenu import ControlMenu

class SinglePlaylistWindow(MainWidget):
    def __init__(self, playlistName, databaseObject, musicEventHandler, parent=None):
        super().__init__(databaseObject, musicEventHandler, parent)

        self.playlistName = playlistName
        self.databaseObject = databaseObject
        self.musicEventHandler = musicEventHandler
        self.parent = parent

        self.setWindowTitle(playlistName)

        self.parent.singleWindowRunning = True

        self.initMenu()

        self.topWidget.refreshPage(self.databaseObject.getSongs(self.playlistName))

        self.show()

    def initMenu(self):
        self.menubar = QMenuBar(self)

        self.fileMenu = FileMenu(False, self)
        self.controlMenu = ControlMenu(self, self)

        self.menubar.addMenu(self.fileMenu)
        self.menubar.addMenu(self.controlMenu)

        self.layout.setMenuBar(self.menubar)
    
    def closeEvent(self, event):
        self.parent.singleWindowRunning = False
        print("Closing single playlist window")
        event.accept()