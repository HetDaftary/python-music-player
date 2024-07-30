import time

from PyQt5.QtCore import QThread
import pygame
from mp3.musicEventHandler import MusicEventHandler
from mutagen.mp3 import MP3

class PlayNextonSongEnd(QThread):
    def __init__(self, parent, eventHandler):
        super().__init__()
        self.eventHandler = eventHandler
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT and self.eventHandler.stopedByUser:
                    print("Song ended, emitting signal to play next song.")
                    self.eventHandler.CUSTOM_SIGNAL.emit(MusicEventHandler.PLAY_NEXT)
                    self.eventHandler.stopedByUser = False
            time.sleep(0.1)  # Prevent the thread from consuming too much CPU

    def stop(self):
        self.running = False