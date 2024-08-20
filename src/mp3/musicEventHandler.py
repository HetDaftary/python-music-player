import os
import shutil
from sys import maxsize

from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot, QMutex, QUrl
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

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
    SET_VOLUME = 10

    MUSIC_CONTROL_SIGNAL = pyqtSignal(int, name = "musicPlayer") # Play/pause and stop music playing.
    PLAY_NEW_SIGNAL = pyqtSignal(int, str, name = "playNewSignal") # To play a song using it's filepath.
    VOLUME_SIGNAL = pyqtSignal(int, int, name = "setVolume") # To set volume to any value.
    SET_SONG_POSITION = pyqtSignal(int, name="setSongPOsition")

    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.parent = parent 
        
        self.player = QMediaPlayer(self)
        self.audioOutput = QAudioOutput(parent=self)
        self.player.setAudioOutput(self.audioOutput)

        self.vol = 0.6

        # Logic parts
        self.isPlaying = False
        self.songName = ""
        self.volume = 60

        self.mutex = QMutex()  # Mutex for thread safety

        self.MUSIC_CONTROL_SIGNAL.connect(self.eventHandlerInt)
        self.PLAY_NEW_SIGNAL.connect(self.playNewSlot)
        self.VOLUME_SIGNAL.connect(self.setVolumeSlot)
        self.SET_SONG_POSITION.connect(self.setPosition)
    
    @staticmethod
    def getDuration(songName):
        audio = MP3(songName)
        return round(audio.info.length * 1000) # Using the milliseconds format.    

    def playPause(self):
        
        if self.isPlaying:
            self.player.pause()
        else:
            self.player.play()
        self.isPlaying = not self.isPlaying
        

    def stopSong(self):
        
        self.player.stop()
        
        self.isPlaying = False
        self.songName = ""

        self.parent.MUSIC_CONTROL_SIGNAL.emit(self.parent.SWITCH_TO_RESUME)
        self.parent.DESELECT_SONG_ON_TABLE.emit()
        self.parent.songPlayingSignal.emit(self.parent.SONG_PLAYING_CODE, "")

    @pyqtSlot(int)
    def setPosition(self, position):
        if self.songName != "":
            self.player.setPosition(position) 

    def getSongPlaying(self):
        return self.songName

    def getPosition(self):
        position = self.player.position()
        return position

    def playNew(self, songName: str):
        self.stopSong() # To stop the player if it is already running.
        # To play new song
        try:
            self.songName = songName

            url = ""
            if songName.startswith("/"):
                url = QUrl.fromLocalFile(songName)  # Replace with the path to your MP3 file
            else:
                url = QUrl.fromLocalFile(os.path.join(os.getcwd(), songName))
            self.player.setSource(url)
            
            self.player.play()
            self.setVolume(self.volume)
            self.parent.songPlayingSignal.emit(self.parent.SONG_PLAYING_CODE, songName)
            self.parent.MUSIC_CONTROL_SIGNAL.emit(self.parent.SWITCH_TO_PAUSE)
        except Exception as e:
            print("Caught exception", e)
            return None

        self.parent.DESELECT_SONG_ON_TABLE.emit()

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
                "NA"
            ]

    @staticmethod
    def writeDataToSong(songName, title, artist, album, year, genre, comment = "NA"):
        if os.path.isfile(songName):
            audio = EasyID3(songName)

            audio['title'] = title
            audio['artist'] = artist
            audio['album'] = album
            audio['date'] = year
            audio['genre'] = genre
            
            audio.save()

    def setVolume(self, vol):
        self.vol = vol
        self.audioOutput.setVolume(round(self.vol))
        

    def stop(self):
        self.stopSong()
        self.quit()

    @pyqtSlot(int)
    def eventHandlerInt(self, value):
        if value == MusicEventHandler.PLAY_PAUSE:
            self.playPause()
            if self.isPlaying:
                self.parent.MUSIC_CONTROL_SIGNAL.emit(self.parent.SWITCH_TO_PAUSE)
            else:
                self.parent.MUSIC_CONTROL_SIGNAL.emit(self.parent.SWITCH_TO_RESUME)
        elif value == MusicEventHandler.STOP:
            self.stopSong()
            
    @pyqtSlot(int, str)
    def playNewSlot(self, value, songName):
        if value == MusicEventHandler.PLAY_SELECTED:
            self.playNew(songName)
            self.parent.MUSIC_CONTROL_SIGNAL.emit(self.parent.SWITCH_TO_PAUSE)

    @pyqtSlot(int, int)
    def setVolumeSlot(self, value, volume):
        self.setVolume(volume)