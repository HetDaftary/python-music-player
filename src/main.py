from PyQt5.QtWidgets import QApplication
from ui.mainwindow import MainWindow
import sys

if __name__ == "__main__":
    app = QApplication(["Music Player"])
    window = MainWindow(app)
    sys.exit(app.exec_())