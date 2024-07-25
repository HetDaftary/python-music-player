import os
import shutil
import pygame

from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from mutagen.easyid3 import EasyID3
from sys import maxsize

class MusicEventHandler(QThread):
    PLAY_NEXT = 0 # These will be catched by slots in MusicEventHandler thread.
    PLAY_PREVIOUS = 1
    PLAY_PAUSE = 2
    PLAY_SELECTED = 3
    STOP = 4 # If the user stops the song.
    PLAY_NEW = 5 # User wants to play something else.
    PLAY_SONG_NOT_IN_LIB = 6
    ADD_A_SONG = 7
    DELETE_A_SONG = 8

    SONG_END = pygame.USEREVENT # If song automatically ends.

    CUSTOM_SIGNAL = pyqtSignal(int, name = "musicPlayer") # Signal to throw for making event.
    PLAY_NEW_SIGNAL = pyqtSignal(int, int, name = "playNewSignal")
    INT_STRING_SIGNAL = pyqtSignal(int, str, name="playSongOutsideLib")

    def __init__(self, songs, parent = None) -> None:
        super().__init__(parent)
        self.parent = parent 
        
        pygame.init()
        pygame.mixer.init()
        self.songs = songs
        self.vol = 0.6

        # Logic parts
        self.isPlaying = False
        self.songIndex = -1
        self.songName = ""
        self.volume = 0.6

        self.CUSTOM_SIGNAL.connect(self.eventHandlerInt)
        self.PLAY_NEW_SIGNAL.connect(self.playNewSlot)
        self.INT_STRING_SIGNAL.connect(self.intStringSignalHandler)

    def playPause(self):
        if self.songIndex == -1 and len(self.songs) > 0:
            self.songIndex = 0
            self.songName = self.songs[self.songIndex]
            pygame.mixer.music.load(self.songs[0]) 
            pygame.mixer.music.set_volume(self.vol) 
            pygame.mixer.music.play() 
            pygame.mixer.music.pause()
            self.parent.songPlayingSignal.emit(self.parent.SONG_PLAYING_CODE, self.songs[self.songIndex])

        if len(self.songs) > 0:
            if self.isPlaying:
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()
            self.isPlaying = not self.isPlaying

    def stopSong(self):
        if self.songIndex != -1:
            pygame.mixer.music.stop()
            self.songName = None
            self.isPlaying = False
            self.songIndex = -1

        self.parent.songPlayingSignal.emit(self.parent.SONG_PLAYING_CODE, "")

    def playNew(self, newIndex):
        self.stopSong() # To stop the player if it is already running.

        # To play new song
        try:
            pygame.mixer.music.load(self.songs[newIndex])
            pygame.mixer.music.play() 
            pygame.mixer.music.set_endevent(self.SONG_END)
            self.setVolume(self.volume)
            self.songIndex = newIndex
            self.parent.songPlayingSignal.emit(self.parent.SONG_PLAYING_CODE, self.songs[self.songIndex])
        except Exception as e:
            print("Caught exception", e)
            return None
        
        self.songIndex = newIndex
        self.songName = self.songs[newIndex]
        self.isPlaying = True

    def getSongPlaying(self):
        return self.songName if self.songName != None else ""

    @staticmethod
    def getSongData(songName):
        if os.path.isfile(songName):
            audio = EasyID3(songName)
            return [
                audio.get('title', ['Unknown Title'])[0], 
                audio.get('artist', ['Unknown Artist'])[0],
                audio.get('album', ['Unknown Album'])[0],
                audio.get('date', ['Unknown Year'])[0],
                audio.get('genre', ['Unknown genre'])[0], 
                audio.get('comment', ['NA'])[0]
            ]

    @staticmethod
    def writeDataToSong(songName, title, artist, album, year, genre, comment):
        if os.path.isfile(songName):
            audio = EasyID3(songName)

            audio['title'] = title
            audio['artist'] = artist
            audio['album'] = album
            audio['date'] = year
            audio['genre'] = genre
            #audio['comment'] = comment # Cannot write comment to a song

            audio.save()

    def setVolume(self, vol):
        vol = max(0, min(vol, 1))
        pygame.mixer.music.set_volume(vol) 

    def playPrevious(self):
        if self.songIndex > -1 and self.songIndex < len(self.songs):  
            self.playNew((self.songIndex - 1) % len(self.songs))
        else:
            self.playNew(0)

    def playNext(self):
        if self.songIndex > -1 and self.songIndex < len(self.songs):    
            self.playNew((self.songIndex + 1) % len(self.songs))
        else:
            self.playNew(0)

    def stop(self):
        self.stopSong()
        pygame.mixer.quit()
        pygame.quit()
        self.quit()

    @pyqtSlot(int)
    def eventHandlerInt(self, value):
        if value == MusicEventHandler.PLAY_NEXT:
            self.playNext()
            self.parent.CUSTOM_SIGNAL.emit(self.parent.SWITCH_TO_PAUSE)
        elif value == MusicEventHandler.PLAY_PREVIOUS:
            self.playPrevious()
            self.parent.CUSTOM_SIGNAL.emit(self.parent.SWITCH_TO_PAUSE)
        elif value == MusicEventHandler.PLAY_PAUSE:
            self.playPause()
            if self.isPlaying:
                self.parent.CUSTOM_SIGNAL.emit(self.parent.SWITCH_TO_PAUSE)
            else:
                self.parent.CUSTOM_SIGNAL.emit(self.parent.SWITCH_TO_PLAY)
        elif value == MusicEventHandler.STOP:
            self.stopSong()
            self.parent.CUSTOM_SIGNAL.emit(self.parent.SWITCH_TO_PLAY)

    @pyqtSlot(int, int)
    def playNewSlot(self, value, songIndex):
        if value == MusicEventHandler.PLAY_SELECTED:
            self.playNew(songIndex)
            self.parent.CUSTOM_SIGNAL.emit(self.parent.SWITCH_TO_PAUSE)

    @pyqtSlot(int, str)
    def intStringSignalHandler(self, val, filePath):
        if val == self.ADD_A_SONG:
            self.addSongToLib(filePath)
        elif val == self.PLAY_SONG_NOT_IN_LIB:
            self.playNotInLib(filePath)
        elif val == self.DELETE_A_SONG:
            self.deleteSongFromLib(filePath)

    def addSongToLib(self, filePath):
        basename = os.path.basename(filePath)
        try:
            shutil.copy(filePath, os.path.join(self.parent.MUSIC_PATH, basename))
            self.songs = self.parent.getSongs()
            self.parent.REFRESH_TOP_WIDGET_SIGNAL.emit()
        except Exception as e:
            print(e)

    def deleteSongFromLib(self, filePath):
        try:    
            os.remove(filePath)
            self.songs.remove(filePath)
            self.parent.REFRESH_TOP_WIDGET_SIGNAL.emit()
        except Exception as e:
            print(e)

    def playNotInLib(self, filePath):
        if os.path.exists(filePath):
            self.stopSong()

            try:
                pygame.mixer.music.load(filePath)
                pygame.mixer.music.play() 
                pygame.mixer.music.set_endevent(self.SONG_END)
                self.setVolume(self.volume)
                self.songIndex = maxsize
                self.isPlaying = [0]
                self.parent.songPlayingSignal.emit(self.parent.SONG_PLAYING_CODE, filePath)
                self.parent.CUSTOM_SIGNAL.emit(self.parent.SWITCH_TO_PAUSE)
            except Exception as e:
                print("Caught exception", e)
                return None