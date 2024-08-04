import sys 
import os
import shutil

from PyQt5.QtWidgets import QVBoxLayout, QWidget, QMessageBox, QFileDialog
from PyQt5.QtCore import QSize, pyqtSignal, pyqtSlot, QDir
from PyQt5.QtGui import QIcon, QColor

# Importing necessary classes for UI
from ui.bottomwidget import BottomWidget
from ui.topwidget import TopWidget

# Importing necessary classes for handling music
from mp3.musicEventHandler import MusicEventHandler

# Import necessary classes for handling database
from sqlite.databasehandler import DatabaseHandler

class MainWidget(QWidget):
    MUSIC_PATH="data/mp3-files" # This is a static variable of this class.
    SWITCH_TO_RESUME = 10 # Values to change UI play pause button. 
    SWITCH_TO_PAUSE = 11 # These will be catched by slots in UI/main thread.
    SWITCH_TO_RESUME = 12
    SONG_PLAYING_CODE = 13 # For the signal to tell about which song is playing.
    REFRESH_SONGS_SIGNAL = 14
    SET_VOLUME = 15
    MUSIC_CONTROL_SIGNAL = pyqtSignal(int, name = "playPauseHandle") # Signal to throw for making event.
    songPlayingSignal = pyqtSignal(int, str, name = "tellsWhichSongIsPlaying") # tells which song is getting played
    REFRESH_TOP_WIDGET_SIGNAL = pyqtSignal(name = "refreshTopWidget") # Refreshes top widget
    DESELECT_SONG_ON_TABLE = pyqtSignal(name = "deselectTheSelectSong")

    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent

        self.songIndex = -1
        self.selectedPlaylist = "library"

        self.currentTheme = "dark.css"

        self.databaseObject = DatabaseHandler()

        # Set layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Setup music handler threads
        self.musicEventHandler = MusicEventHandler(self)

        # Add bottom panel
        self.initBottomWidget()

        # Add top widget
        self.initTopWidget()

        self.layout.addWidget(self.topWidget)
        self.layout.addWidget(self.bottomWidget)

        # Start music handler threads
        self.musicEventHandler.start()

    def getSongs(self):
        return self.databaseObject.getSongs(self.selectedPlaylist)

    def initTopWidget(self):
        self.topWidget = TopWidget(self)

        self.DESELECT_SONG_ON_TABLE.connect(self.handleDeselectSong)
        #self.topWidget.itemChanged.connect(self.changeSongMetaData)
        self.REFRESH_TOP_WIDGET_SIGNAL.connect(self.refreshTopWidget)

    def initBottomWidget(self):
        self.bottomWidget = BottomWidget(self)
        
        self.initButtonActions()

        # Init slot for play pause button.
        self.MUSIC_CONTROL_SIGNAL.connect(self.handlePlayPauseButton)

        # Init song title showing signal
        self.songPlayingSignal.connect(self.handleSongPlaying)

    @pyqtSlot()
    def handleDeselectSong(self):
        self.topWidget.clearSelection()
        
    def initButtonActions(self):
        self.bottomWidget.playSelected.clicked.connect(self.playSelectedButtonAction)
        self.bottomWidget.previousButton.clicked.connect(self.previousButtonAction)
        self.bottomWidget.playPauseButton.clicked.connect(self.playPauseButtonAction)  
        self.bottomWidget.nextButton.clicked.connect(self.nextButtonAction)
        self.bottomWidget.stopButton.clicked.connect(self.stopButtonAction)
        self.bottomWidget.volumeSlider.valueChanged.connect(lambda _: self.musicEventHandler.VOLUME_SIGNAL.emit(self.musicEventHandler.SET_VOLUME, self.bottomWidget.volumeSlider.value()))

    def playSelectedButtonAction(self):
        if self.topWidget.songSelectedByUser == -1:
            QMessageBox.information(self, "Select song", "Please select a song before trying to use this button")
        else:
            self.musicEventHandler.PLAY_NEW_SIGNAL.emit(MusicEventHandler.PLAY_SELECTED, self.topWidget.songs[self.topWidget.songSelectedByUser])  
            self.songIndex = self.topWidget.songSelectedByUser

    def previousButtonAction(self):
        self.songIndex = ((self.songIndex + 1) % len(self.topWidget.songs)) if self.songIndex != -1 else len(self.topWidget.songs) -1
        self.musicEventHandler.PLAY_NEW_SIGNAL.emit(MusicEventHandler.PLAY_SELECTED, self.topWidget.songs[self.songIndex]) 

    def playPauseButtonAction(self):
        if self.songIndex == -1:
            self.songIndex = 0
            self.musicEventHandler.PLAY_NEW_SIGNAL.emit(MusicEventHandler.PLAY_SELECTED, self.topWidget.songs[self.songIndex])
        else:
            self.musicEventHandler.MUSIC_CONTROL_SIGNAL.emit(MusicEventHandler.PLAY_PAUSE)

    def nextButtonAction(self):
        self.songIndex = ((self.songIndex + 1) % len(self.topWidget.songs)) if self.songIndex != -1 else 0
        self.musicEventHandler.PLAY_NEW_SIGNAL.emit(MusicEventHandler.PLAY_SELECTED, self.topWidget.songs[self.songIndex])

    def stopButtonAction(self):
        self.musicEventHandler.MUSIC_CONTROL_SIGNAL.emit(MusicEventHandler.STOP)

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

        self.bottomWidget.songPlayingLabel.setText(f"Playing song : {songTitle}" if songTitle != "" else "")
        self.setSongPlayingSignalButtonBorder()

        songs = self.databaseObject.getSongs(self.selectedPlaylist)

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
                                                                    font-size: 20px;
                                                                    font-weight: bold;
                                                                }
                                                             """)
        elif "dark" in self.currentTheme.lower():
            self.bottomWidget.songPlayingLabel.setStyleSheet("""
                                                                QLabel {
                                                                    border:  2px solid #448aff; 
                                                                    color:  #448aff;
                                                                    font-size: 20px;
                                                                    font-weight: bold;
                                                                }
                                                             """)
        else:
            self.bottomWidget.songPlayingLabel.setStyleSheet("""
                                                                QLabel {
                                                                    border:  2px solid #000000;
                                                                    font-size: 20px;
                                                                    font-weight: bold; 
                                                                }
                                                             """)
    

    @pyqtSlot()
    def refreshTopWidget(self):
        self.topWidget.refreshPage(self.databaseObject.getSongs(self.selectedPlaylist))
        self.parent.show()

    @pyqtSlot(int)
    def handlePlayPauseButton(self, value):
        if value == MainWidget.SWITCH_TO_PAUSE:
            self.bottomWidget.playPauseButton.setIcon(QIcon("data/icons/pause.png"))
            self.playButtonState = MainWidget.SWITCH_TO_PAUSE
        elif value == MainWidget.SWITCH_TO_RESUME:
            self.bottomWidget.playPauseButton.setIcon(QIcon("data/icons/resume.png"))
            self.playButtonState = MainWidget.SWITCH_TO_RESUME
        else:
            self.bottomWidget.playPauseButton.setIcon(QIcon("data/icons/play.png"))
            self.playButtonState = MainWidget.SWITCH_TO_RESUME
        self.bottomWidget.playPauseButton.setIconSize(QSize(32, 32))
        self.bottomWidget.playPauseButton.setFixedSize(QSize(48, 48))

    def changeSongMetaData(self, item):
        print(item.row(), item.row())

        songName = self.databaseObject.getSongs(self.selectedPlaylist)[item.row()]
        rowContent = self.databaseObject.getSongData(songName)
        item.setText(item.text().capitalize())
        rowContent[item.column()] = item.text()
        #MusicEventHandler.writeDataToSong(songName, *rowContent)
        self.databaseObject.writeSongDataToTable(songName, self.selectedPlaylist, *rowContent)

        #self.topWidget.resizeColumnsToContents()

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
            self.musicEventHandler.PLAY_NEW_SIGNAL.emit(MusicEventHandler.PLAY_SELECTED, filePath)
            self.songIndex = sys.maxsize
 
    def addSongWithPath(self, filePath): # Overloading this method so we can also add songs by using drag and drop feature.
        if os.path.join(self.MUSIC_PATH, os.path.basename(filePath)) in self.databaseObject.getSongs(self.selectedPlaylist):
            return None
        
        if filePath and filePath.endswith('.mp3'):
            toPath = os.path.join(self.MUSIC_PATH, os.path.basename(filePath))

            if not os.path.exists(toPath):
                shutil.copy(filePath, toPath)
        
        self.databaseObject.writeSongDataToTable(self.selectedPlaylist, toPath, *self.musicEventHandler.getSongData(toPath))
        self.refreshTopWidget()
    
    def addSong(self):
        filePath, _ = self.getOpenFileName("Add a song")
        if filePath != "" and filePath != None:
            self.addSongWithPath(filePath)

    def deleteSong(self):
        songs = self.databaseObject.getSongs(self.selectedPlaylist)
        
        collectRows = set()

        if self.topWidget.selectedItems():
            for i in self.topWidget.selectedItems():
                collectRows.add(i.row())

            for i in collectRows:
                songName = songs[i]
                self.databaseObject.deleteSongData(self.selectedPlaylist, songName)

                if self.selectedPlaylist == "library":
                    os.remove(songName)
        
        self.refreshTopWidget()
