from ui.horizontalslider import HorizontalSlider

class SongPositionSlider(HorizontalSlider):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.parent.setPosition()
