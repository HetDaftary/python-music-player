from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QSize

from ui.horizontalslider import HorizontalSlider

class VolumeSlider(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        self.setMaximumWidth(160)

        self.volumeIcon = QLabel()
        self.volumeIcon.setPixmap(QPixmap("data/icons/speaker.png").scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.volumeIcon.setFixedSize(QSize(48, 48))
        self.volumeIcon.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.layout.addWidget(self.volumeIcon)

        self.horizontalSlider = HorizontalSlider(self)

        self.horizontalSlider.setRange(0, 100)
        self.horizontalSlider.setValue(60)
        self.horizontalSlider.setMaximumWidth(100)

        self.layout.addWidget(self.horizontalSlider)
