import sys

from PyQt5.QtWidgets import QMainWindow, QMenuBar, QApplication, QSplitter, QWidget, QVBoxLayout
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot

# Importing necessary classes for UI
from ui.filemenu import FileMenu
from ui.mainwidget import MainWidget
from ui.leftpanel import LeftPanel

# Importing necessary classes for handling music
from mp3.musicEventHandler import MusicEventHandler

# Import necessary classes for handling database
from sqlite.databasehandler import DatabaseHandler

class MainWindow(QMainWindow):
    MUSIC_PATH="data/mp3-files" # This is a static variable of this class.
    SWITCH_TO_RESUME = 10 # Values to change UI play pause button. 
    SWITCH_TO_PAUSE = 11 # These will be catched by slots in UI/main thread.
    SWITCH_TO_RESUME = 12
    SONG_PLAYING_CODE = 13 # For the signal to tell about which song is playing.
    REFRESH_SONGS_SIGNAL = 14
    SET_VOLUME = 15
    MUSIC_CONTROL_SIGNAL = pyqtSignal(int, name = "playPauseHandle") # Signal to throw for making event.
    songPlayingSignal = pyqtSignal(int, str, name = "tellsWhichSongIsPlaying") # tells which song is getting played
    DESELECT_SONG_ON_TABLE = pyqtSignal(name = "deselectTheSelectSong")

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

        self.selectedPlaylist = "Library"

        # Init database 
        self.databaseObject = DatabaseHandler()

        # Init music player
        self.musicEventHandler = MusicEventHandler(self)

        # Set left panel and main widget
        self.mainWidget = MainWidget(self.databaseObject, self.musicEventHandler, self)
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

        # Init signals 
        self.initSignals()

        # Show main window
        self.show()

    def initSignals(self):
        # Init top widget signals
        self.DESELECT_SONG_ON_TABLE.connect(self.handleDeselectSong)

        # Init bottom widget signals
        self.MUSIC_CONTROL_SIGNAL.connect(self.handlePlayPauseButton)
        self.songPlayingSignal.connect(self.handleSongPlaying)

    @pyqtSlot()
    def handleDeselectSong(self):
        self.mainWidget.handleDeselectSong()

    @pyqtSlot(int)
    def handlePlayPauseButton(self, value):
        self.mainWidget.handlePlayPauseButton(value)

    @pyqtSlot(int, str)
    def handleSongPlaying(self, value, songName):
        self.mainWidget.handleSongPlaying(value, songName)

    # Defining this to stop pygame thread.
    def closeEvent(self, event):
        self.mainWidget.musicEventHandler.stop()
        self.mainWidget.musicEventHandler.wait()
        self.mainWidget.databaseObject.cur.close()
        self.mainWidget.databaseObject.conn.close()
        QApplication.quit()

    def initMenu(self):
        self.menubar = QMenuBar(self)
        self.fileMenu = FileMenu(parent=self) # This class has 2 optional variables so I need to write which variable should self be assigned to 
        self.menubar.addMenu(self.fileMenu)
        self.setMenuBar(self.menubar)

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
