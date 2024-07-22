from PyQt5.QtWidgets import QMainWindow
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

        # Show main window
        self.show()

    # Defining this to stop pygame thread.
    def closeEvent(self, event):
        self.mainWidget.musicEventHandler.stop()
        self.mainWidget.musicEventHandler.wait()
        self.mainWidget.databaseObject.cur.close()
        self.mainWidget.databaseObject.conn.close()
        event.accept()

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