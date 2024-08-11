import sys

from PyQt5.QtWidgets import QMainWindow, QMenuBar, QApplication, QSplitter, QWidget, QVBoxLayout
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot

# Importing necessary classes for UI
from ui.filemenu import FileMenu
from ui.controlmenu import ControlMenu
from ui.mainwidget import MainWidget
from ui.leftpanel import LeftPanel
from ui.singleplaylistwindow import SinglePlaylistWindow

# Importing necessary classes for handling music
from mp3.musicEventHandler import MusicEventHandler
from mp3.musicpositionthread import MusicPositionThread

# Import necessary classes for handling database
from sqlite.databasehandler import DatabaseHandler

class MainWindow(QMainWindow):
    MUSIC_PATH="data/mp3-files" # This is a static variable of this class.
    SWITCH_TO_PLAY = 10 # Values to change UI play pause button. 
    SWITCH_TO_PAUSE = 11 # These will be catched by slots in UI/main thread.
    SWITCH_TO_RESUME = 12
    SONG_PLAYING_CODE = 13 # For the signal to tell about which song is playing.
    REFRESH_SONGS_SIGNAL = 14
    SET_VOLUME = 15

    MUSIC_POSITION_UPDATE = 100 # Position update given
    MUSIC_END_CODE = 101 # Music ends naturally
    MUSIC_STOP_CODE = 102 # Music stopped by user

    MUSIC_CONTROL_SIGNAL = pyqtSignal(int, name = "playPauseHandle") # Signal to throw for making event.
    songPlayingSignal = pyqtSignal(int, str, name = "tellsWhichSongIsPlaying") # tells which song is getting played
    DESELECT_SONG_ON_TABLE = pyqtSignal(name = "deselectTheSelectSong")
    musicPositionSignal = pyqtSignal(int, int, name = "givesMusicPosition") # Song 

    def __init__(self, app, argv):
        super().__init__()
        self.handleArgv(argv)

        # Set size
        self.app = app
        screenSize = self.app.primaryScreen().size() 
        self.resize(screenSize.width() // 2, screenSize.height() // 2)


        # Init database 
        self.databaseObject = DatabaseHandler()

        # Init music player
        self.musicEventHandler = MusicEventHandler(self)
        self.musicPositionThread = MusicPositionThread(self.musicEventHandler, self)

        # Set left panel and main widget
        self.mainWidget = MainWidget(self.databaseObject, self.musicEventHandler, self)
        
        if self.singlePlaylist:
            self.setWindowTitle(self.selectedPlaylist)
            self.setCentralWidget(self.mainWidget)
        else:
            self.setWindowTitle("My Tunes")
            self.leftPanel = LeftPanel(self.mainWidget.databaseObject, self)

            self.splitter = QSplitter(Qt.Horizontal)

            self.centralWidget = QWidget(self)
            self.layout = QVBoxLayout()
            self.centralWidget.setLayout(self.layout)

            self.splitter.addWidget(self.leftPanel)
            self.splitter.addWidget(self.mainWidget)

            # Set the stretch factors
            self.splitter.setStretchFactor(0, 1)
            self.splitter.setStretchFactor(1, 7)

            self.layout.addWidget(self.splitter)

            self.setCentralWidget(self.centralWidget)

        # Start music handler threads
        self.musicEventHandler.start()
        self.musicPositionThread.start()

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

    def handleArgv(self, argv):
        if len(argv) > 1:
            for arg in argv:
                if arg.startswith("--single-playlist="):
                    self.selectedPlaylist = arg.split("=")[1]
                    self.singlePlaylist = True
                    return None
        self.selectedPlaylist = "Library"
        self.singlePlaylist = False

    def initSignals(self):
        # Init top widget signals
        self.DESELECT_SONG_ON_TABLE.connect(self.handleDeselectSong)

        # Init bottom widget signals
        self.MUSIC_CONTROL_SIGNAL.connect(self.handlePlayPauseButton)
        self.songPlayingSignal.connect(self.handleSongPlaying)

        # Init other signals
        self.musicPositionSignal.connect(self.songPositionHandle)

    @pyqtSlot(int, int)
    def songPositionHandle(self, val, position):
        self.mainWidget.songPositionHandle(val, position)
        
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
        if not self.singlePlaylist and self.leftPanel.singleWindowRunning:
            self.leftPanel.singlePlaylistWindow.stop()

        self.musicPositionThread.stop()
        self.musicPositionThread.wait()
        self.musicEventHandler.stop()
        self.musicEventHandler.wait()
        self.databaseObject.cur.close()
        self.databaseObject.conn.close()
        event.accept()

    def initMenu(self):
        self.menubar = QMenuBar(self)
        self.fileMenu = FileMenu(not self.singlePlaylist, self) # This class has 2 optional variables so I need to write which variable should self be assigned to 
        self.menubar.addMenu(self.fileMenu)

        self.fileMenu.openSongAction.triggered.connect(self.mainWidget.openAndPlayAMp3)
        self.fileMenu.exitAppAction.triggered.connect(lambda _: self.closeEvent(0))
        self.fileMenu.addSongAction.triggered.connect(self.mainWidget.addSong)
        self.fileMenu.deleteSongAction.triggered.connect(self.mainWidget.deleteSong)
        if not self.singlePlaylist and self.fileMenu.isMainMenu:
            self.fileMenu.createPlaylistAction.triggered.connect(self.leftPanel.createPlaylist)

        self.controlMenu = ControlMenu(self.mainWidget, self)
        self.menubar.addMenu(self.controlMenu)
        
        self.setMenuBar(self.menubar)

    def initFonts(self):
        fontId = QFontDatabase.addApplicationFont("data/fonts/Aller_Rg.ttf")

        # Check if font loading was successful (optional)
        if fontId == -1:
            print("Failed to load font!")

    def initStyleSheet(self):
        with open('data/css/dark.css', 'r') as f:
            stylesheet = f.read()
            self.app.setStyleSheet(stylesheet)
