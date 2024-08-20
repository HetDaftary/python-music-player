import os

from PyQt6.QtCore import QThread, pyqtSlot, pyqtSignal

class RefreshPlaylistApp(QThread):
    HANDLE_PLAYLIST_CHANGE = pyqtSignal(str, name="handlePlaylistChange") 
    def __init__(self, parent = None):
        super().__init__(parent)
        self.parent = parent
        self.delay = 100 # Sleep time in milliseconds
        self.selectedPlaylist = ""
        self.HANDLE_PLAYLIST_CHANGE.connect(self.changePlaylist)
        self.running = True
        self.changePlaylist(self.parent.selectedPlaylist)

    @pyqtSlot(str)
    def changePlaylist(self, playlistName):
        self.selectedPlaylist = playlistName
        if not os.path.exists(f"data/temp/{self.selectedPlaylist}.txt"):
            with open(f"data/temp/{self.selectedPlaylist}.txt", "w") as f:
                pass
            with open("data/temp/Library.txt", "w") as filePtr:
                filePtr.write("refresh")

        self.lastMTime = os.path.getmtime(f"data/temp/{self.selectedPlaylist}.txt")
        self.lastMTimeLib = self.lastMTime if self.selectedPlaylist.lower() == "library" else os.path.getmtime("data/temp/Library.txt")

    def processFileChanged(self, path):
        print("method called")
        if self.selectedPlaylist.lower() in path.lower(): 
            print("emitting change")
            self.parent.mainWidget.REFRESH_SONGS.emit()

    def run(self):
        while self.running:
            if os.path.getmtime(f"data/temp/{self.selectedPlaylist}.txt") > self.lastMTime:
                self.parent.REFRESH_SONGS.emit()
            if self.selectedPlaylist != "library" and os.path.getmtime("data/temp/Library.txt") > self.lastMTimeLib:
                self.parent.REFRESH_SONGS.emit()
            
            self.lastMTime = os.path.getmtime(f"data/temp/{self.selectedPlaylist}.txt")
            if self.selectedPlaylist != "library":
                self.lastMTimeLib = os.path.getmtime("data/temp/Library.txt")

            self.msleep(self.delay)
    
    def stop(self):
        self.running = False
        self.finished.emit()