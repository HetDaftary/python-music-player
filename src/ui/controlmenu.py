from PyQt5.QtWidgets import QMenu, QAction, QCheckBox

from ui.mainwidget import MainWidget

class ControlMenu(QMenu):
    def __init__(self, mainWidget: MainWidget, parent = None):
        super().__init__("Control", parent)
        self.parent = parent
        
        self.mainWidget = mainWidget

        self.playButton = QAction("Play") # Plays selected song
        self.nextButton = QAction("Next") # Next song button
        self.previousButton = QAction("Previous") # Previous song button
        self.playRecentButton = QMenu("Play Recent") # Play recent button
        self.increaseVolume = QAction("Increase volume") 
        self.decreaseVolume = QAction("Decrease volume")
        self.shuffle = QAction("Shuffle")
        self.shuffle.setCheckable(True)
        self.repeatSong = QAction("Repeat")
        self.repeatSong.setCheckable(True)

        self.addRecentSongs()

        self.playButton.triggered.connect(self.mainWidget.playSelectedButtonAction)
        self.nextButton.triggered.connect(self.mainWidget.nextButtonAction)
        self.previousButton.triggered.connect(self.mainWidget.previousButtonAction)

        self.increaseVolume.triggered.connect(self.mainWidget.increaseVolume)
        self.decreaseVolume.triggered.connect(self.mainWidget.decreaseVolume)

        self.shuffle.triggered.connect(lambda _: self.mainWidget.setShuffle(self.shuffle.isChecked()))
        self.repeatSong.triggered.connect(lambda _: self.mainWidget.setRepeatSongs(self.repeatSong.isChecked()))

        self.addAction(self.playButton)
        self.addAction(self.nextButton)
        self.addAction(self.previousButton)
        self.addMenu(self.playRecentButton)
        self.addSeparator()
        self.addAction(self.increaseVolume)
        self.addAction(self.decreaseVolume)
        self.addSeparator()
        self.addAction(self.shuffle)
        self.addAction(self.repeatSong)

    def addRecentSongs(self):
        self.recentSongs = []

        self.playRecentButton.clear()

        for songName in self.parent.databaseObject.getLastSongs():
            self.recentSongs.append(QAction(songName))
            self.recentSongs[-1].triggered.connect(lambda _, songName = songName: self.playSelected(songName))
            self.playRecentButton.addAction(self.recentSongs[-1])

    def playSelected(self, songName):
        for i in range(0, len(self.mainWidget.topWidget.songs)):
            if songName == self.mainWidget.topWidget.songs[i]:
                self.mainWidget.topWidget.songSelectedByUser = i
                break
        self.mainWidget.playSelectedButtonAction()