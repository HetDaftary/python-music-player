from PyQt5.QtWidgets import QApplication
from ui.mainwindow import MainWindow
import sys
import signal

def closeApplication(signal, frame):
    QApplication.quit()

def main():
    for sing in [signal.SIGINT, signal.SIGTERM, signal.SIGABRT]:
        signal.signal(sing, closeApplication)
    
    app = QApplication(["My Tunes"])    
    window = MainWindow(app, sys.argv)
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()