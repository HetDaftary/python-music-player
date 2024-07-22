import sys 
import os

from PyQt5.QtWidgets import QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtCore import QSize, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon

# Importing necessary classes for UI
from ui.bottomwidget import BottomWidget
from ui.topwidget import TopWidget

# Importing necessary classes for handling music
from mp3.musicEventHandler import MusicEventHandler

# Import necessary classes for handling database
from sqlite.databasehandler import DatabaseHandler

class MainWidget(QWidget):
    MUSIC_PATH="data/mp3-files" # This is a static variable of this class.
    SWITCH_TO_PLAY = 10 # Values to change UI play pause button. 
    SWITCH_TO_PAUSE = 11 # These will be catched by slots in UI/main thread.
    SONG_PLAYING_CODE = 12 # For the signal to tell about which song is playing.

    CUSTOM_SIGNAL = pyqtSignal(int, name = "playPauseHandle") # Signal to throw for making event.
    songPlayingSignal = pyqtSignal(int, str, name = "tellsWhichSongIsPlaying") # tells which song is getting played

    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent

        self.databaseObject = DatabaseHandler()

        # Set layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        

        # Setup music handler threads
        self.musicEventHandler = MusicEventHandler(MainWidget.getSongs(), self)

        # Start music handler threads
        self.musicEventHandler.start()

        # Add bottom panel
        self.initBottomWidget()

        # Add top widget
        self.initTopWidget()

        self.layout.addWidget(self.topWidget)
        self.layout.addWidget(self.bottomWidget)

    @staticmethod
    def getSongs():
        return [os.path.join(MainWidget.MUSIC_PATH, x) for x in os.listdir(MainWidget.MUSIC_PATH) if x.endswith(".mp3")]            

    def initTopWidget(self):
        self.topWidget = TopWidget(MainWidget.getSongs(), self)

        # Save meta data edited
        self.topWidget.itemChanged.connect(self.changeSongMetaData)

    def initBottomWidget(self):
        self.bottomWidget = BottomWidget(self)
        
        self.initButtonActions()

        # Init slot for play pause button.
        self.CUSTOM_SIGNAL.connect(self.handlePlayPauseButton)

        # Init song title showing signal
        self.songPlayingSignal.connect(self.handleSongPlaying)

    def initButtonActions(self):
        self.bottomWidget.playSelected.clicked.connect(self.playSelectedButtonAction)
        self.bottomWidget.previousButton.clicked.connect(self.previousButtonAction)
        self.bottomWidget.playPauseButton.clicked.connect(self.playPauseButtonAction)  
        self.bottomWidget.nextButton.clicked.connect(self.nextButtonAction)
        self.bottomWidget.stopButton.clicked.connect(self.stopButtonAction)

    def playSelectedButtonAction(self):
        if self.topWidget.songSelectedByUser == -1:
            QMessageBox.information(self, "Select song", "Please select a song before trying to use this button")
        else:
            self.musicEventHandler.PLAY_NEW_SIGNAL.emit(MusicEventHandler.PLAY_SELECTED, self.topWidget.songSelectedByUser)    

    def previousButtonAction(self):
        self.musicEventHandler.CUSTOM_SIGNAL.emit(MusicEventHandler.PLAY_PREVIOUS)

    def playPauseButtonAction(self):
        self.musicEventHandler.CUSTOM_SIGNAL.emit(MusicEventHandler.PLAY_PAUSE)

    def nextButtonAction(self):
        self.musicEventHandler.CUSTOM_SIGNAL.emit(MusicEventHandler.PLAY_NEXT)

    def stopButtonAction(self):
        self.musicEventHandler.CUSTOM_SIGNAL.emit(MusicEventHandler.STOP)

    @pyqtSlot(int, str)
    def handleSongPlaying(self, value, songTitle):
        self.bottomWidget.songPlayingLabel.setText(songTitle)

    @pyqtSlot(int)
    def handlePlayPauseButton(self, value):
        if value == MainWidget.SWITCH_TO_PAUSE:
            self.bottomWidget.playPauseButton.setIcon(QIcon("data/icons/pause.png"))
        else:
            self.bottomWidget.playPauseButton.setIcon(QIcon("data/icons/play.png"))
        self.bottomWidget.playPauseButton.setIconSize(QSize(32, 32))
        self.bottomWidget.playPauseButton.setFixedSize(QSize(48, 48))

    def changeSongMetaData(self, item):
        songName = self.getSongs()[item.row()]
        rowContent = MusicEventHandler.getSongData(songName)
        
        rowContent[item.column()] = item.text()
        MusicEventHandler.writeDataToSong(songName, *rowContent)
        self.databaseObject.writeSongDataToTable(songName, *rowContent)

        self.topWidget.resizeColumnsToContents()