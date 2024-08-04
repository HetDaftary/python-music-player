import sys

from PyQt5.QtWidgets import QMainWindow, QMenu, QAction, QMenuBar, QApplication, QSplitter, QWidget, QVBoxLayout
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtCore import Qt

from ui.mainwidget import MainWidget
from ui.leftpanel import LeftPanel

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()

        self.setWindowTitle("My Tunes")

        # Set size
        self.app = app
        screenSize = self.app.primaryScreen().size() 
        self.resize(screenSize.width() // 2, screenSize.height() // 2)

        self.centralWidget = QWidget(self)
        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)

        # Set main widget
        self.mainWidget = MainWidget(self)
        self.leftPanel = LeftPanel(self.mainWidget.databaseObject, self)

        self.splitter = QSplitter(Qt.Horizontal)

        self.splitter.addWidget(self.leftPanel)
        self.splitter.addWidget(self.mainWidget)

        # Set the stretch factors
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 7)

        self.layout.addWidget(self.splitter)

        self.setCentralWidget(self.centralWidget)

        # Init fonts
        self.initFonts()

        # Init menu bar.
        self.initMenu()

        # Initialize style sheet
        self.initStyleSheet()

        # Show main window
        self.show()

    # Defining this to stop pygame thread.
    def closeEvent(self, event):
        self.mainWidget.musicEventHandler.stop()
        self.mainWidget.musicEventHandler.wait()
        self.mainWidget.databaseObject.cur.close()
        self.mainWidget.databaseObject.conn.close()
        QApplication.quit()

    def initMenu(self):
        self.menubar = QMenuBar(self)

        self.fileMenu = QMenu("File")
        
        self.openSongAction = QAction("Open and play a song")
        self.exitAppAction = QAction("Close")

        self.addSongAction = QAction("Add song to library")
        self.deleteSongAction = QAction("Delete currently selected song")
        self.createPlaylistAction = QAction("Create a playlist")

        self.fileMenu.addAction(self.openSongAction)
        self.fileMenu.addAction(self.exitAppAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.addSongAction)
        self.fileMenu.addAction(self.deleteSongAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.createPlaylistAction)

        self.menubar.addMenu(self.fileMenu)

        self.setMenuBar(self.menubar)

        self.openSongAction.triggered.connect(self.mainWidget.openAndPlayAMp3)
        self.exitAppAction.triggered.connect(self.closeAppMenuAction)
        self.addSongAction.triggered.connect(self.mainWidget.addSong)
        self.deleteSongAction.triggered.connect(self.mainWidget.deleteSong)
        self.createPlaylistAction.triggered.connect(self.leftPanel.createPlaylist)

    def closeAppMenuAction(self):
        self.closeEvent(0)

    def initFonts(self):
        fontId = QFontDatabase.addApplicationFont("data/fonts/Aller_Rg.ttf")

        # Check if font loading was successful (optional)
        if fontId == -1:
            print("Failed to load font!")

    def initStyleSheet(self):
        with open('data/css/dark.css', 'r') as f:
            stylesheet = f.read()
            self.app.setStyleSheet(stylesheet)
