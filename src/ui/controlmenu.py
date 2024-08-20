from PyQt6.QtWidgets import QMenu
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QKeySequence

from ui.mainwidget import MainWidget

class ControlMenu(QMenu):
    def __init__(self, mainWidget: MainWidget, parent = None):
        super().__init__("Control", parent)
        self.parent = parent
        
        self.mainWidget = mainWidget

        self.playButton = QAction("Play") # Plays selected song
        self.playButton.setShortcut(QKeySequence("Space"))
        self.nextButton = QAction("Next") # Next song button
        self.nextButton.setShortcut(QKeySequence("Ctrl+Right"))
        self.previousButton = QAction("Previous") # Previous song button
        self.previousButton.setShortcut(QKeySequence("Ctrl+Left"))
        self.playRecentButton = QMenu("Play Recent") # Play recent button
        self.goToCurrentSong = QAction("Go to Current Song")
        self.goToCurrentSong.setShortcut(QKeySequence("Ctrl+L"))
        self.increaseVolume = QAction("Increase volume")
        self.increaseVolume.setShortcut(QKeySequence("Ctrl+I")) 
        self.decreaseVolume = QAction("Decrease volume")
        self.decreaseVolume.setShortcut(QKeySequence("Ctrl+D"))
        self.shuffle = QAction("Shuffle")
        self.shuffle.setCheckable(True)
        self.repeatSong = QAction("Repeat")
        self.repeatSong.setCheckable(True)

        self.addRecentSongs()

        self.playButton.triggered.connect(self.mainWidget.playSelectedButtonAction)
        self.nextButton.triggered.connect(self.mainWidget.nextButtonAction)
        self.previousButton.triggered.connect(self.mainWidget.previousButtonAction)
        self.goToCurrentSong.triggered.connect(self.mainWidget.goToCurrentSong)

        self.increaseVolume.triggered.connect(self.mainWidget.increaseVolume)
        self.decreaseVolume.triggered.connect(self.mainWidget.decreaseVolume)

        self.shuffle.triggered.connect(lambda _: self.mainWidget.setShuffle(self.shuffle.isChecked()))
        self.repeatSong.triggered.connect(lambda _: self.mainWidget.setRepeatSongs(self.repeatSong.isChecked()))

        self.addAction(self.playButton)
        self.addAction(self.nextButton)
        self.addAction(self.previousButton)
        self.addMenu(self.playRecentButton)
        self.addAction(self.goToCurrentSong)
        self.addSeparator()
        self.addAction(self.increaseVolume)
        self.addAction(self.decreaseVolume)
        self.addSeparator()
        self.addAction(self.shuffle)
        self.addAction(self.repeatSong)

    def addRecentSongs(self):
        self.recentSongNames = self.parent.databaseObject.getLastSongs()
        self.recentSongs = []

        titleToSongName = dict()
        for songName in self.recentSongNames:
            title = self.parent.databaseObject.getSongTitle(songName)
            titleToSongName[title] = songName

        self.playRecentButton.clear()

        for songTitle in titleToSongName:
            self.recentSongs.append(QAction(songTitle))
            self.recentSongs[-1].triggered.connect(lambda _, songName = titleToSongName[songTitle]: self.playSelected(songName))
            self.playRecentButton.addAction(self.recentSongs[-1])

    def playSelected(self, songName):
        for i in range(0, len(self.mainWidget.topWidget.songs)):
            if songName == self.mainWidget.topWidget.songs[i]:
                self.mainWidget.topWidget.songSelectedByUser = i
                break
        self.mainWidget.playSelectedButtonAction()