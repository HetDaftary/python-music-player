import os

class SinglePlaylistWindow():
    def __init__(self, playlistName):
        self.playlistName = playlistName
        self.singleWindowRunning = True

        os.system(f"python3 src/main.py --single-playlist {self.playlistName}")

    def __del__(self):
        self.singleWindowRunning = False
