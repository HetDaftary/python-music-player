import sys
import signal

from PyQt6.QtWidgets import QApplication
from ui.mainwindow import MainWindow

def closeApplication(signal, frame):
    QApplication.quit()

def main():
    for sing in [signal.SIGINT, signal.SIGTERM, signal.SIGABRT]:
        signal.signal(sing, closeApplication)
    
    app = QApplication(["My Tunes"])    
    window = MainWindow(app, sys.argv)
    
    app.exec()

if __name__ == "__main__":
    main()