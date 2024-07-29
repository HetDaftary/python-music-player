import sys 
import os

from PyQt5.QtWidgets import QVBoxLayout, QWidget, QMessageBox, QFileDialog
from PyQt5.QtCore import QSize, pyqtSignal, pyqtSlot, QDir
from PyQt5.QtGui import QIcon, QColor

# Importing necessary classes for UI
from ui.bottomwidget import BottomWidget
from ui.topwidget import TopWidget
from ui.deleteSongWidget import DeleteSongWidget

# Importing necessary classes for handling music
from mp3.musicEventHandler import MusicEventHandler

# Import necessary classes for handling database
from sqlite.databasehandler import DatabaseHandler

class MainWidget(QWidget):
    MUSIC_PATH="data/mp3-files" # This is a static variable of this class.
    SWITCH_TO_PLAY = 10 # Values to change UI play pause button. 
    SWITCH_TO_PAUSE = 11 # These will be catched by slots in UI/main thread.
    SONG_PLAYING_CODE = 12 # For the signal to tell about which song is playing.
    REFRESH_SONGS_SIGNAL = 13
    CUSTOM_SIGNAL = pyqtSignal(int, name = "playPauseHandle") # Signal to throw for making event.
    songPlayingSignal = pyqtSignal(int, str, name = "tellsWhichSongIsPlaying") # tells which song is getting played
    REFRESH_TOP_WIDGET_SIGNAL = pyqtSignal(name = "refreshTopWidget") # Refreshes top widget

    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent

        self.currentTheme = "dark.css"

        self.databaseObject = DatabaseHandler()

        # Set layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Setup music handler threads
        self.musicEventHandler = MusicEventHandler(MainWidget.getSongs(), self)

        # Add bottom panel
        self.initBottomWidget()

        # Add top widget
        self.initTopWidget()

        self.layout.addWidget(self.topWidget)
        self.layout.addWidget(self.bottomWidget)

        # Start music handler threads
        self.musicEventHandler.start()

    @staticmethod
    def getSongs():
        return [os.path.join(MainWidget.MUSIC_PATH, x) for x in os.listdir(MainWidget.MUSIC_PATH) if x.endswith(".mp3")]            

    def initTopWidget(self):
        self.topWidget = TopWidget(MainWidget.getSongs(), self)

        # Save meta data edited
        self.topWidget.itemChanged.connect(self.changeSongMetaData)
        self.REFRESH_TOP_WIDGET_SIGNAL.connect(self.refreshTopWidget)

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
    def handleSongPlaying(self, value, songName):
        songTitle = ""
        if songName != "" and songName != None:
            songData = self.databaseObject.getSongData(songName)
            if len(songData) != 0:
                songTitle = songData[0][0]
            else:
                songData = MusicEventHandler.getSongData(songName)
                songTitle = songData[0]

        self.bottomWidget.songPlayingLabel.setText(songTitle)
        self.setSongPlayingSignalButtonBorder()

        songs = self.getSongs()

        for i in range(len(songs)):
            if songName == songs[i]:
                self.highlightRow(i)
                return None
            
        self.highlightRow(sys.maxsize)

    def highlightRow(self, row):
        for i in range(self.topWidget.rowCount()):
            if i == row:    
                for col in range(self.topWidget.columnCount()):
                    self.topWidget.item(i, col).setBackground(QColor(82, 83, 186))  # #24c9c7
            else:
                for col in range(self.topWidget.columnCount()):
                    self.topWidget.item(i, col).setBackground(QColor(49, 54, 59))  # #31363b
        

    def setSongPlayingSignalButtonBorder(self):    
        if self.bottomWidget.songPlayingLabel.text().strip() == "":
            self.bottomWidget.songPlayingLabel.setStyleSheet("""
                                                                QLabel {
                                                                    border: none;
                                                                }
                                                             """)
        elif "dark" in self.currentTheme.lower():
            self.bottomWidget.songPlayingLabel.setStyleSheet("""
                                                                QLabel {
                                                                    border:  2px solid #448aff; 
                                                                    color:  #448aff;
                                                                }
                                                             """)
        else:
            self.bottomWidget.songPlayingLabel.setStyleSheet("""
                                                                QLabel {
                                                                    border:  2px solid #000000; 
                                                                }
                                                             """)
    

    @pyqtSlot()
    def refreshTopWidget(self):
        self.topWidget.refreshPage(self.getSongs())
        self.parent.show()

    @pyqtSlot(int)
    def handlePlayPauseButton(self, value):
        if value == MainWidget.SWITCH_TO_PAUSE:
            self.bottomWidget.playPauseButton.setIcon(QIcon("data/icons/pause.png"))
        else:
            self.bottomWidget.playPauseButton.setIcon(QIcon("data/icons/resume.png"))
        self.bottomWidget.playPauseButton.setIconSize(QSize(32, 32))
        self.bottomWidget.playPauseButton.setFixedSize(QSize(48, 48))

    def changeSongMetaData(self, item):
        songName = self.getSongs()[item.row()]
        rowContent = MusicEventHandler.getSongData(songName)
        item.setText(item.text().capitalize())
        rowContent[item.column()] = item.text()
        MusicEventHandler.writeDataToSong(songName, *rowContent)
        self.databaseObject.writeSongDataToTable(songName, *rowContent)

        self.topWidget.resizeColumnsToContents()

    def getOpenFileName(self, name):
        options = QFileDialog.Options()
        homeDir = QDir.homePath()  # Get the user's home directory
        filePath, _ = QFileDialog.getOpenFileName(self,
                                                   name,
                                                   homeDir,
                                                   "MP3 Files (*.mp3);;All Files (*)",
                                                   options=options)
        
        return filePath, _

    def openAndPlayAMp3(self):
        filePath, _ = self.getOpenFileName( "Open and play a song")
        
        if filePath:
            self.musicEventHandler.INT_STRING_SIGNAL.emit(self.musicEventHandler.PLAY_SONG_NOT_IN_LIB, filePath)
        else:
            print("pressed cancel")
 
    def addSongWithPath(self, filePath): # Overloading this method so we can also add songs by using drag and drop feature.
        if os.path.join(self.MUSIC_PATH, os.path.basename(filePath)) in self.getSongs():
            return None
        
        if filePath:
            self.musicEventHandler.INT_STRING_SIGNAL.emit(self.musicEventHandler.ADD_A_SONG, filePath)
        else:
            print("pressed cancel")
    
    def addSong(self):
        filePath, _ = self.getOpenFileName("Add a song")
        if filePath != "" and filePath != None:
            self.addSongWithPath(filePath)

    def deleteSong(self):
        self.selectedEntries = []
        
        # This widget is suppused to give us the song to delete in the above list
        self.deleteSongWidget = DeleteSongWidget(self)
        self.deleteSongWidget.exec_()

        for songName in self.selectedEntries:
            self.musicEventHandler.INT_STRING_SIGNAL.emit(self.musicEventHandler.DELETE_A_SONG, os.path.join(self.MUSIC_PATH, songName))

            # Delete entry from database
            self.databaseObject.deleteSongData(songName)
