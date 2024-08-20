from PyQt6.QtCore import Qt

from ui.horizontalslider import HorizontalSlider

class SongPositionSlider(HorizontalSlider):
    def __init__(self, musicEventHandler, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.musicEventHandler = musicEventHandler

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Calculate the new position based on the click location

            pos = event.pos()
            sliderRect = self.rect()

            normalizedPos = (pos.x() - sliderRect.left()) / sliderRect.width()
            value = normalizedPos * (self.maximum() - self.minimum()) + self.minimum()

            # Set the slider's value to the new position
            self.setPosition(int(value))
            self.parent.updatePosition(int(value))
            event.accept()
        else:
            super().mousePressEvent(event)
        
    def setPosition(self, newPosition):
        self.musicEventHandler.setPosition(newPosition)
