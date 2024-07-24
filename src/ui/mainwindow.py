from PyQt5.QtWidgets import QMainWindow, QMenu, QAction, QMenuBar, QApplication, QFileDialog
from PyQt5.QtGui import QFontDatabase

from ui.mainwidget import MainWidget

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()

        # Set size
        self.app = app
        screenSize = self.app.primaryScreen().size() 
        self.resize(screenSize.width() // 2, screenSize.height() // 2)

        # Set main widget
        self.mainWidget = MainWidget(self)
        self.setCentralWidget(self.mainWidget)

        # Init fonts
        self.initFonts()

        # Initialize style sheet
        self.initStyleSheet()

        # Init menu bar.
        self.initMenu()

        # Show main window
        self.show()

    # Defining this to stop pygame thread.
    def closeEvent(self, event):
        self.mainWidget.musicEventHandler.stop()
        self.mainWidget.musicEventHandler.wait()
        self.mainWidget.databaseObject.cur.close()
        self.mainWidget.databaseObject.conn.close()
        QApplication.quit()


    def initMenu(self):
        self.menubar = QMenuBar(self)

        self.fileMenu = QMenu("File")
        
        self.openSongAction = QAction("Open and play a song")
        self.exitAppAction = QAction("Close")
        self.addSongAction = QAction("Add a song")
        self.deleteSongAction = QAction("Delete a song")

        self.fileMenu.addAction(self.openSongAction)
        self.fileMenu.addAction(self.exitAppAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.addSongAction)
        self.fileMenu.addAction(self.deleteSongAction)

        self.menubar.addMenu(self.fileMenu)

        self.setMenuBar(self.menubar)

        self.openSongAction.triggered.connect(self.mainWidget.openAndPlayAMp3)
        self.exitAppAction.triggered.connect(self.closeAppMenuAction)
        self.addSongAction.triggered.connect(self.mainWidget.addSong)
        self.deleteSongAction.triggered.connect(self.mainWidget.deleteSong)

    def closeAppMenuAction(self):
        self.closeEvent(0)

    def initFonts(self):
        font_id = QFontDatabase.addApplicationFont("data/fonts/Aller_Rg.ttf")

        # Check if font loading was successful (optional)
        if font_id != -1:
            print("Font loaded successfully")
        else:
            print("Failed to load font!")

    def initStyleSheet(self):
        with open('data/css/dark.css', 'r') as f:
            stylesheet = f.read()
            self.app.setStyleSheet(stylesheet)