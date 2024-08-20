from PyQt6.QtWidgets import QSlider
from PyQt6.QtCore import Qt

class HorizontalSlider(QSlider):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setOrientation(Qt.Orientation.Horizontal)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Calculate the new position based on the click location

            pos = event.pos()
            slider_rect = self.rect()

            normalized_pos = (pos.x() - slider_rect.left()) / slider_rect.width()
            value = normalized_pos * (self.maximum() - self.minimum()) + self.minimum()

            # Set the slider's value to the new position
            self.setValue(int(value))
            event.accept()
        else:
            super().mousePressEvent(event)