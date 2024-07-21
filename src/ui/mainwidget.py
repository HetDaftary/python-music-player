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

class MainWidget(QWidget):
    MUSIC_PATH="data/mp3-files" # This is a static variable of this class.
    SWITCH_TO_PLAY = 10 # Values to change UI play pause button. 
    SWITCH_TO_PAUSE = 11 # These will be catched by slots in UI/main thread.

    CUSTOM_SIGNAL = pyqtSignal(int, name = "playPauseHandle") # Signal to throw for making event.

    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent

        # Set layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Setup music handler threads
        self.musicEventHandler = MusicEventHandler(MainWidget.getSongs(), self)

        # Start music handler threads
        self.musicEventHandler.start()

        # Add top widget
        self.initTopWidget()

        # Add bottom panel
        self.initBottomWidget()

        # Init slot for play pause button.
        self.CUSTOM_SIGNAL.connect(self.handlePlayPauseButton)

    @staticmethod
    def getSongs():
        return [os.path.join(MainWidget.MUSIC_PATH, x) for x in os.listdir(MainWidget.MUSIC_PATH) if x.endswith(".mp3")]            

    def initTopWidget(self):
        self.topWidget = TopWidget(MainWidget.getSongs(), self)
        self.layout.addWidget(self.topWidget)

    def initBottomWidget(self):
        self.bottomWidget = BottomWidget(self)
        self.layout.addWidget(self.bottomWidget)
        self.initButtonActions()

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

    @pyqtSlot(int)
    def handlePlayPauseButton(self, value):
        if value == MainWidget.SWITCH_TO_PAUSE:
            self.bottomWidget.playPauseButton.setIcon(QIcon("data/icons/pause.png"))
        else:
            self.bottomWidget.playPauseButton.setIcon(QIcon("data/icons/play.png"))
        self.bottomWidget.playPauseButton.setIconSize(QSize(32, 32))
        self.bottomWidget.playPauseButton.setFixedSize(QSize(48, 48))