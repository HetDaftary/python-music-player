from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

from ui.horizontalslider import HorizontalSlider

class VolumeSlider():
    def __init__(self, parent=None):
        self.parent = parent
        
        self.volumeIcon = QPushButton()
        self.volumeIcon.setIcon(QIcon("data/icons/speaker.png"))
        self.volumeIcon.setIconSize(QSize(32, 32))
        self.volumeIcon.setFixedSize(QSize(48, 48))
        self.volumeIcon.clicked.connect(self.volumeIconHandle)
        self.horizontalSlider = HorizontalSlider(self.parent)

        self.isMuted = False

        self.horizontalSlider.setRange(0, 100)
        self.horizontalSlider.setValue(60)
        self.horizontalSlider.setMaximumWidth(100)

    def volumeIconHandle(self):
        self.parent.volumeIconHandle()