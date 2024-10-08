from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QSizePolicy, QLabel
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon

from ui.volumeslider import VolumeSlider

class BottomWidget(QWidget):
    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent

        self.layout = QVBoxLayout()
        
        self.buttonsWidget = QWidget()
        self.setMaximumHeight(150)
        self.buttonsLayout = QHBoxLayout()
        self.buttonsWidget.setLayout(self.buttonsLayout)
        
        self.buttonsLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter) 
        self.setLayout(self.layout)
        self.buttonsWidget.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.songPlayingLabel = QLabel("")
        self.songPlayingLabel.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.songPlayingLabel.setMaximumHeight(self.buttonsWidget.height())
        self.songPlayingLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.songPlayingLabel)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter) 

        self.playSelected = QPushButton()
        self.playSelected.setIcon(QIcon("data/icons/play.png"))
        self.playSelected.setIconSize(QSize(32, 32))
        self.playSelected.setFixedSize(QSize(48, 48))
        self.buttonsLayout.addWidget(self.playSelected)
        
        self.previousButton = QPushButton()
        self.previousButton.setIcon(QIcon("data/icons/previous.png"))
        self.previousButton.setIconSize(QSize(32, 32))
        self.previousButton.setFixedSize(QSize(48, 48))
        self.buttonsLayout.addWidget(self.previousButton)
        
        self.playPauseButton = QPushButton()
        self.playPauseButton.setIcon(QIcon("data/icons/resume.png"))
        self.playPauseButton.setIconSize(QSize(32, 32))
        self.playPauseButton.setFixedSize(QSize(48, 48))
        self.buttonsLayout.addWidget(self.playPauseButton)
        
        self.nextButton = QPushButton()
        self.nextButton.setIcon(QIcon("data/icons/next.png"))
        self.nextButton.setIconSize(QSize(32, 32))
        self.nextButton.setFixedSize(QSize(48, 48))
        self.buttonsLayout.addWidget(self.nextButton)
        
        self.stopButton = QPushButton()
        self.stopButton.setIcon(QIcon("data/icons/stop.png"))
        self.stopButton.setIconSize(QSize(32, 32))
        self.stopButton.setFixedSize(QSize(48, 48))
        self.buttonsLayout.addWidget(self.stopButton)

        self.volumeSlider = VolumeSlider(self)
        #self.buttonsLayout.addWidget(self.volumeSlider)

        self.buttonsLayout.addWidget(self.volumeSlider.volumeIcon)
        self.buttonsLayout.addWidget(self.volumeSlider.horizontalSlider)

        self.layout.addWidget(self.buttonsWidget)
    
    def volumeIconHandle(self):
        self.parent.volumeIconHandle()