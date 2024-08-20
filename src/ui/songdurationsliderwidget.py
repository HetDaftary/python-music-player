from PyQt6.QtWidgets import QLabel, QWidget, QSizePolicy, QHBoxLayout

from ui.songpositionslider import SongPositionSlider

class SongDurationSliderWidget(QWidget):
    def __init__(self, musicEventHandler, parent=None):
        super().__init__(parent)
        self.parent = parent

        self.musicEventHandler = musicEventHandler
        
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.currentPosLabel = QLabel("0:00:00")
        self.currentPosLabel.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum))
        self.layout.addWidget(self.currentPosLabel)

        self.horizontalSlider = SongPositionSlider(self.musicEventHandler, self)
        self.layout.addWidget(self.horizontalSlider)

        self.endPosLabel = QLabel("0:00:00")
        self.endPosLabel.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum))
        self.layout.addWidget(self.endPosLabel)

        self.duration = 0

    @staticmethod
    def convertToTime(timeInMilliseconds):
        time = timeInMilliseconds // 1000
        hours = f"{time // 3600}"
        time = time % 3600
        minutes = f"{time // 60}"
        minutes = f"{minutes}" if len(minutes) > 1 else f"0{minutes}" 
        seconds = f"{time % 60}"
        seconds = f"{seconds}" if len(seconds) > 1 else f"0{seconds}"

        return f"{hours}:{minutes}:{seconds}"

    def setForNewSong(self, duration):
        self.duration = duration
        durationTime = self.convertToTime(duration)
        self.endPosLabel.setText(durationTime) 
        self.endPosLabel.adjustSize()

        self.currentPosLabel.setText("0:00:00")
        self.currentPosLabel.adjustSize()

        self.horizontalSlider.setRange(0, duration)
        self.horizontalSlider.setValue(0)

    def updatePosition(self, position):
        currentTime = self.convertToTime(position)
        self.currentPosLabel.setText(currentTime)
        self.currentPosLabel.adjustSize()
        self.horizontalSlider.setValue(position)

        remainingTime = self.convertToTime(self.duration - position)
        self.endPosLabel.setText(remainingTime)
        self.endPosLabel.adjustSize()
