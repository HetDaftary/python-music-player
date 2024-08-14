from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize

from ui.horizontalslider import HorizontalSlider

class VolumeSlider(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        self.setMaximumWidth(160)

        self.volumeIcon = QPushButton()
        self.volumeIcon.setIcon(QIcon("data/icons/speaker.png"))
        self.volumeIcon.setIconSize(QSize(32, 32))
        self.volumeIcon.setFixedSize(QSize(48, 48))
        self.volumeIcon.clicked.connect(self.volumeIconHandle)
        self.layout.addWidget(self.volumeIcon)

        self.horizontalSlider = HorizontalSlider(self)

        self.isMuted = False

        self.horizontalSlider.setRange(0, 100)
        self.horizontalSlider.setValue(60)
        self.horizontalSlider.setMaximumWidth(100)

        self.layout.addWidget(self.horizontalSlider)

    def volumeIconHandle(self):
        self.parent.volumeIconHandle()