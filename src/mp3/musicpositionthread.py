import pygame
import time

from PyQt5.QtCore import QThread
from mutagen.mp3 import MP3

class MusicPositionThread(QThread):
    def __init__(self, musicEventHandler, parent = None):
        super().__init__(parent=None)
        self.parent = parent
        self.musicEventHandler = musicEventHandler
        self.lastSong = ""
        self.lastPos = -1
        self.lastSongDuration = 0
        self.running = True
        self.delay = 100

    def setDelay(self, delay):
        self.delay = delay

    def getDelay(self):
        return self.delay

    @staticmethod
    def getDuration(songName):
        audio = MP3(songName)
        return round(audio.info.length * 1000) # Using the milliseconds format.
    
    def run(self):
        while self.running:
            currentPos = pygame.mixer.music.get_pos()
            if self.lastPos != -1 and currentPos == -1:
                # A song that was playing stopped due to stop button by user or song end
                print(self.lastSongDuration, self.lastPos, (self.lastSongDuration - self.lastPos) / 1000, self.delay)
                if self.lastSongDuration - self.lastPos <= 2 * self.delay:
                    # Song ended naturally without user interaction
                    print("song stopped naturally")
                    #self.parent.musicPositionSignal.emit(self.parent.MUSIC_END_CODE, currentPos)
                else:
                    # Song stopped by user
                    print("song stopped by user")
                    #self.parent.musicPositionSignal.emit(self.parent.MUSIC_STOP_CODE, currentPos)
                self.lastSong =  ""
                self.lastSongDuration = 0
            elif self.lastPos == -1 and currentPos != -1:
                # A song started
                # To updated last song name, duration etc.
                self.lastSong = self.musicEventHandler.songName
                self.lastSongDuration = self.getDuration(self.lastSong)

                print("song playing:", self.lastSong)
                print("song duration:", self.lastSongDuration)

            self.lastPos = currentPos

            self.msleep(self.delay) # We sleep for delay amount of milliseconds
        print("Music positioning thread ended")

    def stop(self):
        self.running = False