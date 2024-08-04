from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QSizePolicy, QLabel, QSlider
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap

class BottomWidget(QWidget):
    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent

        self.layout = QVBoxLayout()
        
        self.buttonsWidget = QWidget()
        self.setMaximumHeight(150)
        self.buttonsLayout = QHBoxLayout()
        self.buttonsWidget.setLayout(self.buttonsLayout)
        
        self.buttonsLayout.setAlignment(Qt.AlignHCenter) 
        self.setLayout(self.layout)
        self.buttonsWidget.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.songPlayingLabel = QLabel("")
        self.songPlayingLabel.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.songPlayingLabel.setMaximumHeight(self.buttonsWidget.height())
        self.songPlayingLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.songPlayingLabel)
        self.layout.setAlignment(Qt.AlignBottom | Qt.AlignHCenter) 

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

        self.volumeIcon = QLabel()
        self.volumeIcon.setPixmap(QPixmap("data/icons/speaker.png").scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.volumeIcon.setFixedSize(QSize(48, 48))
        self.volumeIcon.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.buttonsLayout.addWidget(self.volumeIcon)

        self.volumeSlider = QSlider(self.buttonsWidget)
        self.volumeSlider.setOrientation(Qt.Horizontal)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(60)
        self.volumeSlider.setMaximumWidth(100)
        self.buttonsLayout.addWidget(self.volumeSlider)

        self.layout.addWidget(self.buttonsWidget)