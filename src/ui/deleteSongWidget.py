import os

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QListWidget, QApplication

class DeleteSongWidget(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.mainWidget = self.parent

        self.listOfSongs = QListWidget()
        self.listOfSongs.addItems([os.path.basename(x) for x in self.mainWidget.getSongs()])
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(self.listOfSongs)

        self.deleteSongButton = QPushButton("Delete")
        self.layout.addWidget(self.deleteSongButton)
        self.deleteSongButton.clicked.connect(self.deleteSongFromMenuButtonAction)

        screenSize = QApplication.primaryScreen().size() 
        self.resize(screenSize.width() // 2, screenSize.height() // 2)

    def deleteSongFromMenuButtonAction(self):
        self.mainWidget.selectedEntries.extend([x.text() for x in self.listOfSongs.selectedItems()])
        self.accept()