from PyQt5.QtWidgets import QMenuBar

from ui.mainwidget import MainWidget
from ui.filemenu import FileMenu
from ui.controlmenu import ControlMenu

class SinglePlaylistWindow(MainWidget):
    def __init__(self, databaseObject, musicEventHandler, parent = None):
        super().__init__(databaseObject, musicEventHandler, parent)

        self.databaseObject = databaseObject
        self.musicEventHandler = musicEventHandler
        self.parent = parent

        self.initMenu()

        self.hide()

    def startWithPlayist(self):
        pass

    def initMenu(self):
        self.menuBar = QMenuBar()
        self.fileMenu = FileMenu(isMainMenu = False, parent = self)
        self.controlMenu = ControlMenu(self, self)
        self.menuBar.addMenu(self.fileMenu)
        self.layout.setMenuBar(self.menuBar)
