import sys 
import os
import shutil
import random

from PyQt5.QtWidgets import QVBoxLayout, QWidget, QMessageBox, QFileDialog
from PyQt5.QtCore import QSize, QDir
from PyQt5.QtGui import QIcon, QColor

# Importing necessary classes for UI
from ui.bottomwidget import BottomWidget
from ui.topwidget import TopWidget
from ui.songdurationsliderwidget import SongDurationSliderWidget

class MainWidget(QWidget):
    def __init__(self, databaseObject, musicEventHandler, parent = None):
        super().__init__()
        self.parent = parent

        self.songIndex = -1
        self.currentTheme = "dark.css"
        self.shuffleSongs = False
        self.repeatSongs = False

        self.databaseObject = databaseObject

        # Set layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Setup music handler threads
        self.musicEventHandler = musicEventHandler

        # Add bottom panel
        self.initBottomWidget()

        # Add top widget
        self.initTopWidget()

        # Init song slider
        self.initSongSlider()

        self.layout.addWidget(self.songDurationSliderWidget)
        self.layout.addWidget(self.topWidget)
        self.layout.addWidget(self.bottomWidget)

    def initSongSlider(self):
        self.songDurationSliderWidget = SongDurationSliderWidget(self.musicEventHandler, self)

    def initTopWidget(self):
        self.topWidget = TopWidget(self)

    def initBottomWidget(self):
        self.bottomWidget = BottomWidget(self)
        self.initButtonActions()

    #@pyqtSlot()
    def handleDeselectSong(self):
        self.topWidget.clearSelection()
    
    def setVolume(self, newVol = -1):
        if (type(newVol) == float):
            newVol = round(newVol) # Rount new volume to nearest integer

        if newVol == -1:
            newVol = self.bottomWidget.volumeSlider.horizontalSlider.value()
        self.musicEventHandler.VOLUME_SIGNAL.emit(self.musicEventHandler.SET_VOLUME, newVol)
        self.bottomWidget.volumeSlider.horizontalSlider.setValue(newVol)

    def increaseVolume(self):
        self.setVolume(max(min(self.bottomWidget.volumeSlider.horizontalSlider.value() * 1.05, 100), 0))
    
    def decreaseVolume(self):
        self.setVolume(max(min(self.bottomWidget.volumeSlider.horizontalSlider.value() * 0.95, 100), 0))

    def setRepeatSongs(self, checkState):
        self.repeatSongs = checkState

    def setShuffle(self, checkState):
        self.shuffleSongs = checkState
    
    def initButtonActions(self):
        self.bottomWidget.playSelected.clicked.connect(self.playSelectedButtonAction)
        self.bottomWidget.previousButton.clicked.connect(self.previousButtonAction)
        self.bottomWidget.playPauseButton.clicked.connect(self.playPauseButtonAction)  
        self.bottomWidget.nextButton.clicked.connect(self.nextButtonAction)
        self.bottomWidget.stopButton.clicked.connect(self.stopButtonAction)
        self.bottomWidget.volumeSlider.horizontalSlider.valueChanged.connect(self.setVolume)

    def playSelectedButtonAction(self):
        if self.topWidget.songSelectedByUser == -1:
            if self.shuffleSongs:
                self.topWidget.songSelectedByUser = random.randint(0, len(self.topWidget.songs) - 1)
            else:    
                self.topWidget.songSelectedByUser = 0
        
        self.songIndex = self.topWidget.songTitleToIndex[self.topWidget.item(self.topWidget.songSelectedByUser, 0).text()]

        self.musicEventHandler.PLAY_NEW_SIGNAL.emit(self.musicEventHandler.PLAY_SELECTED, self.topWidget.songs[self.songIndex])  
        self.databaseObject.addSongToHistory(self.topWidget.songs[self.songIndex])
        self.songDurationSliderWidget.setForNewSong(self.musicEventHandler.getDuration(self.topWidget.songs[self.songIndex]))
        self.parent.controlMenu.addRecentSongs()

    def previousButtonAction(self):
        if self.shuffleSongs:
            self.songIndex = random.randint(0, len(self.topWidget.songs) - 1)
        else:
            self.songIndex = ((self.songIndex - 1) % len(self.topWidget.songs)) if self.songIndex != -1 else len(self.topWidget.songs) -1
        self.musicEventHandler.PLAY_NEW_SIGNAL.emit(self.musicEventHandler.PLAY_SELECTED, self.topWidget.songs[self.songIndex]) 
        self.databaseObject.addSongToHistory(self.topWidget.songs[self.songIndex])
        self.songDurationSliderWidget.setForNewSong(self.musicEventHandler.getDuration(self.topWidget.songs[self.songIndex]))
        self.parent.controlMenu.addRecentSongs()

    def playPauseButtonAction(self):
        if self.songIndex == -1:
            self.songIndex = 0
            self.musicEventHandler.PLAY_NEW_SIGNAL.emit(self.musicEventHandler.PLAY_SELECTED, self.topWidget.songs[self.songIndex])
        else:
            self.musicEventHandler.MUSIC_CONTROL_SIGNAL.emit(self.musicEventHandler.PLAY_PAUSE)
        self.parent.controlMenu.addRecentSongs()

    def nextButtonAction(self):
        if self.shuffleSongs:
            self.songIndex = random.randint(0, len(self.topWidget.songs) - 1)
        else:    
            self.songIndex = ((self.songIndex + 1) % len(self.topWidget.songs)) if self.songIndex != -1 else 0
        self.musicEventHandler.PLAY_NEW_SIGNAL.emit(self.musicEventHandler.PLAY_SELECTED, self.topWidget.songs[self.songIndex])
        self.songDurationSliderWidget.setForNewSong(self.musicEventHandler.getDuration(self.topWidget.songs[self.songIndex]))
        self.databaseObject.addSongToHistory(self.topWidget.songs[self.songIndex])
        self.parent.controlMenu.addRecentSongs()

    def stopButtonAction(self):
        self.musicEventHandler.MUSIC_CONTROL_SIGNAL.emit(self.musicEventHandler.STOP)
        self.songDurationSliderWidget.setForNewSong(0)

    #@pyqtSlot(int, int)
    def songPositionHandle(self, val, position):
        if val == self.parent.MUSIC_END_CODE:
            if self.repeatSongs:
                if self.songIndex == -1:
                    # Play selected function uses song selected by user parameter to decide which song to play.
                    self.topWidget.songSelectedByUser = random.randint(0, len(self.topWidget.songs)) if self.shuffleSongs else 0
                self.playSelectedButtonAction()
            else:
                # Play next song if repeat songs is not set 
                self.nextButtonAction()
        else:
            self.songDurationSliderWidget.updatePosition(position)

    #@pyqtSlot(int, str)
    def handleSongPlaying(self, value, songName):
        songTitle = ""
        if songName != "" and songName != None:
            songData = self.databaseObject.getSongData(songName)
            if len(songData) != 0:
                songTitle = songData[0][0]
            else:
                songData = self.musicEventHandler.getSongData(songName)
                songTitle = songData[0]

        self.bottomWidget.songPlayingLabel.setText(f"{songTitle}" if songTitle != "" else "")
        self.setSongPlayingSignalButtonBorder()

        self.topWidget.refreshPage()

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
    

    #@pyqtSlot()
    def refreshTopWidget(self):
        self.topWidget.refreshPage()
        self.parent.show()

    #@pyqtSlot(int)
    def handlePlayPauseButton(self, value):
        if value == self.parent.SWITCH_TO_PAUSE:
            self.bottomWidget.playPauseButton.setIcon(QIcon("data/icons/pause.png"))
            self.playButtonState = self.parent.SWITCH_TO_PAUSE
        elif value == self.parent.SWITCH_TO_RESUME:
            self.bottomWidget.playPauseButton.setIcon(QIcon("data/icons/resume.png"))
            self.playButtonState = self.parent.SWITCH_TO_RESUME
        else:
            self.bottomWidget.playPauseButton.setIcon(QIcon("data/icons/play.png"))
            self.playButtonState = self.parent.SWITCH_TO_RESUME
        self.bottomWidget.playPauseButton.setIconSize(QSize(32, 32))
        self.bottomWidget.playPauseButton.setFixedSize(QSize(48, 48))

    def changeSongMetaData(self, item):
        print(item.row(), item.row())

        songName = self.databaseObject.getSongs(self.parent.selectedPlaylist)[item.row()]
        rowContent = self.databaseObject.getSongData(songName)
        item.setText(item.text().capitalize())
        rowContent[item.column()] = item.text()
        #MusicEventHandler.writeDataToSong(songName, *rowContent)
        self.databaseObject.writeSongDataToTable(songName, self.parent.selectedPlaylist, *rowContent)

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
            self.musicEventHandler.PLAY_NEW_SIGNAL.emit(self.musicEventHandler.PLAY_SELECTED, filePath)
            self.songIndex = sys.maxsize
            self.songDurationSliderWidget.setForNewSong(self.musicEventHandler.getDuration(filePath))
 
    def addSongWithPath(self, filePath): # Overloading this method so we can also add songs by using drag and drop feature.
        if os.path.join(self.parent.MUSIC_PATH, os.path.basename(filePath)) in self.databaseObject.getSongs(self.parent.selectedPlaylist):
            return None
        
        if filePath and filePath.endswith('.mp3'):
            toPath = os.path.join(self.parent.MUSIC_PATH, os.path.basename(filePath))

            if not os.path.exists(toPath):
                shutil.copy(filePath, toPath)
        
        self.databaseObject.writeSongDataToTable(self.parent.selectedPlaylist, toPath, *self.musicEventHandler.getSongData(toPath))
        self.refreshTopWidget()
    
    def addSong(self):
        filePath, _ = self.getOpenFileName("Add a song")
        if filePath != "" and filePath != None:
            self.addSongWithPath(filePath)

    def addToPlaylist(self, playlistName):
        collectRows = set()
        for i in self.topWidget.selectedItems():
            collectRows.add(i.row())
        
        songs = self.databaseObject.getSongs(self.parent.selectedPlaylist)
        
        for i in collectRows:
            songName = songs[i]
            self.databaseObject.addToPlaylist(playlistName, songName)

    def deleteSong(self):
        songs = self.databaseObject.getSongs(self.parent.selectedPlaylist)
        collectRows = set()

        if self.topWidget.selectedItems():
            for i in self.topWidget.selectedItems():
                collectRows.add(i.row())

            for i in collectRows:
                songName = songs[i]
                self.databaseObject.deleteSongData(self.parent.selectedPlaylist, songName)

                if self.parent.selectedPlaylist.lower() == "library":
                    os.remove(songName)
                    self.databaseObject.deleteSongFromHistory(songName)    
                    self.parent.controlMenu.addRecentSongs()
        self.refreshTopWidget()
