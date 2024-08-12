from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt

class HorizontalSlider(QSlider):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setOrientation(Qt.Horizontal)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Calculate the new position based on the click location
            if self.orientation() == Qt.Horizontal:
                new_value = self.minimum() + (self.maximum() - self.minimum()) * event.x() / self.width()
            else:
                new_value = self.minimum() + (self.maximum() - self.minimum()) * (self.height() - event.y()) / self.height()
            
            # Set the slider's value to the new position
            self.setValue(int(new_value))
            event.accept()
        else:
            super().mousePressEvent(event)