import os

from PyQt5.QtCore import QThread

class MusicPositionThread(QThread):
    def __init__(self, musicEventHandler, parent = None):
        super().__init__(parent=None)
        self.parent = parent
        self.musicEventHandler = musicEventHandler
        self.lastSong = ""
        self.lastPos = 0
        self.lastSongDuration = 0
        self.running = True
        self.delay = 1000

        self.toSetPosition = False

    def setDelay(self, delay):
        self.delay = delay

    def getDelay(self):
        return self.delay

    def run(self):
        while self.running:
            currentPos = self.musicEventHandler.getPosition()
            if currentPos == self.lastSongDuration:
                self.parent.musicPositionSignal.emit(self.parent.MUSIC_END_CODE, currentPos)
                self.lastSong =  ""
                self.lastSongDuration = 0
            elif self.lastPos != 0 and currentPos == 0:
                # Song stopped by user
                self.parent.musicPositionSignal.emit(self.parent.MUSIC_STOP_CODE, currentPos)
                self.lastSong =  ""
                self.lastSongDuration = 0
            elif (self.lastPos == 0 and currentPos != 0) or (self.lastPos > currentPos):
                # A song started
                # To updated last song name, duration etc
                self.lastSong = self.musicEventHandler.songName
                self.lastPos = 0
                self.lastSongDuration = self.musicEventHandler.getDuration(self.lastSong) if os.path.exists(self.lastSong) else 0 
                self.parent.musicPositionSignal.emit(self.parent.MUSIC_POSITION_UPDATE, currentPos)
            elif self.lastSong !=  "":
                # If any song is playing keep updating the position counter
                self.parent.musicPositionSignal.emit(self.parent.MUSIC_POSITION_UPDATE, currentPos)

            self.lastPos = currentPos
            self.msleep(self.delay) # We sleep for delay amount of milliseconds
    
    def stop(self):
        self.running = False
