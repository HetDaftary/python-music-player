import sys

from PyQt5.QtWidgets import QMainWindow, QMenu, QAction, QMenuBar, QApplication, QSplitter, QWidget, QVBoxLayout
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtCore import Qt

from ui.filemenu import FileMenu
from ui.mainwidget import MainWidget
from ui.leftpanel import LeftPanel

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()

        self.setWindowTitle("My Tunes")

        # Set size
        self.app = app
        screenSize = self.app.primaryScreen().size() 
        self.resize(screenSize.width() // 2, screenSize.height() // 2)

        self.centralWidget = QWidget(self)
        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)

        # Set main widget
        self.mainWidget = MainWidget(self)
        self.leftPanel = LeftPanel(self.mainWidget.databaseObject, self)

        self.splitter = QSplitter(Qt.Horizontal)

        self.splitter.addWidget(self.leftPanel)
        self.splitter.addWidget(self.mainWidget)

        # Set the stretch factors
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 7)

        self.layout.addWidget(self.splitter)

        self.setCentralWidget(self.centralWidget)

        # Init fonts
        self.initFonts()

        # Init menu bar.
        self.initMenu()

        # Initialize style sheet
        self.initStyleSheet()

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
        self.fileMenu = FileMenu("File", self)
        self.menubar.addMenu(self.fileMenu)
        self.setMenuBar(self.menubar)

    def closeAppMenuAction(self):
        self.closeEvent(0)

    def initFonts(self):
        fontId = QFontDatabase.addApplicationFont("data/fonts/Aller_Rg.ttf")

        # Check if font loading was successful (optional)
        if fontId == -1:
            print("Failed to load font!")

    def initStyleSheet(self):
        with open('data/css/dark.css', 'r') as f:
            stylesheet = f.read()
            self.app.setStyleSheet(stylesheet)
