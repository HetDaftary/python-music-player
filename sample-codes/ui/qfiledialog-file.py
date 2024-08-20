import sys
from PyQt6.QtWidgets import QApplication, QFileDialog, QWidget
from PyQt6.QtCore import QDir

class FileDialogDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Open file dialog on start
        self.openFileNameDialog()

    def openFileNameDialog(self):
        # Open the file dialog
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        home_dir = QDir.homePath()  # Get the user's home directory
        file_name, _ = QFileDialog.getOpenFileName(self,
                                                   "QFileDialog.getOpenFileName()",
                                                   home_dir,
                                                   "MP3 Files (*.mp3);;All Files (*)",
                                                   options=options)
        if file_name:
            print(f"Selected file: {file_name}")
        else:
            print("No file selected or dialog was canceled")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileDialogDemo()
    ex.show()
    sys.exit(app.exec_())