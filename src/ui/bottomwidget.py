from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSizePolicy
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon

class BottomWidget(QWidget):
    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent

        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignBottom | Qt.AlignHCenter) 
        self.setLayout(self.layout)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))

        self.playSelected = QPushButton(" Play seelected ")
        self.playSelected.setFixedHeight(48)
        self.playSelected.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum))
        self.layout.addWidget(self.playSelected)
        
        self.previousButton = QPushButton()
        self.previousButton.setIcon(QIcon("data/icons/previous.png"))
        self.previousButton.setIconSize(QSize(32, 32))
        self.previousButton.setFixedSize(QSize(48, 48))
        self.layout.addWidget(self.previousButton)
        
        self.playPauseButton = QPushButton()
        self.playPauseButton.setIcon(QIcon("data/icons/play.png"))
        self.playPauseButton.setIconSize(QSize(32, 32))
        self.playPauseButton.setFixedSize(QSize(48, 48))
        self.layout.addWidget(self.playPauseButton)
        
        self.nextButton = QPushButton()
        self.nextButton.setIcon(QIcon("data/icons/next.png"))
        self.nextButton.setIconSize(QSize(32, 32))
        self.nextButton.setFixedSize(QSize(48, 48))
        self.layout.addWidget(self.nextButton)
        
        self.stopButton = QPushButton()
        self.stopButton.setIcon(QIcon("data/icons/stop.png"))
        self.stopButton.setIconSize(QSize(32, 32))
        self.stopButton.setFixedSize(QSize(48, 48))
        self.layout.addWidget(self.stopButton)
