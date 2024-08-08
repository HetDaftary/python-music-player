from PyQt5.QtWidgets import QLabel, QWidget, QSizePolicy, QHBoxLayout

import pygame

from ui.horizontalslider import HorizontalSlider

class SongDurationSliderWidget(QWidget):
    def __init__(self, musicEventHandler, parent=None):
        super().__init__(parent)
        self.parent = parent

        self.musicEventHandler = musicEventHandler
        
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.currentPosLabel = QLabel("00:00")
        self.currentPosLabel.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        self.layout.addWidget(self.currentPosLabel)

        self.horizontalSlider = HorizontalSlider(self)
        self.horizontalSlider.valueChanged.connect(self.setPosition)
        self.layout.addWidget(self.horizontalSlider)

        self.endPosLabel = QLabel("00:00")
        self.endPosLabel.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        self.layout.addWidget(self.endPosLabel)

    @staticmethod
    def convertToTime(timeInMilliseconds):
        time = timeInMilliseconds // 1000

        minutes = f"{time // 60}"
        minutes = f"{minutes}" if len(minutes) > 1 else f"0{minutes}" 
        seconds = f"{time % 60}"
        seconds = f"{seconds}" if len(seconds) > 1 else f"0{seconds}"

        return f"{minutes}:{seconds}"

    def setPosition(self):
        self.musicEventHandler.setPosition(self.horizontalSlider.value())

    def setForNewSong(self, duration):
        durationTime = self.convertToTime(duration)
        self.endPosLabel.setText(durationTime) 
        self.endPosLabel.adjustSize()

        self.currentPosLabel.setText("00:00")
        self.currentPosLabel.adjustSize()

        self.horizontalSlider.setRange(0, duration)
        self.horizontalSlider.setValue(0)

    def updatePosition(self, position):
        self.horizontalSlider.blockSignals(True)
        currentTime = self.convertToTime(position)
        self.currentPosLabel.setText(currentTime)
        self.currentPosLabel.adjustSize()
        self.horizontalSlider.setValue(position)
        self.horizontalSlider.blockSignals(False)