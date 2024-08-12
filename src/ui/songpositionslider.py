from PyQt5.QtCore import Qt

from ui.horizontalslider import HorizontalSlider

class SongPositionSlider(HorizontalSlider):
    def __init__(self, musicEventHandler, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.musicEventHandler = musicEventHandler

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Calculate the new position based on the click location
            if self.orientation() == Qt.Horizontal:
                new_value = self.minimum() + (self.maximum() - self.minimum()) * event.x() / self.width()
            else:
                new_value = self.minimum() + (self.maximum() - self.minimum()) * (self.height() - event.y()) / self.height()
            
            # Set the slider's value to the new position
            self.setPosition(int(new_value))
            #self.setValue(int(new_value))
            self.parent.updatePosition(int(new_value))
            event.accept()
        else:
            super().mousePressEvent(event)
    
    def setPosition(self, newPosition):
        self.musicEventHandler.setPosition(newPosition)
