
import sys
from PyQt6.QtCore import QMutex, QMutexLocker, QThread, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel

class Worker(QThread):
    # Signal to emit the result
    resultReady = pyqtSignal(int)

    def __init__(self, mutex):
        super().__init__()
        self.mutex = mutex

    def run(self):
        # Simulate work that requires mutual exclusion
        for i in range(5):
            self.do_work(i)
            self.msleep(1000)

    def do_work(self, value):
        # Lock the mutex before accessing the shared resource
        self.mutex.lock()
        try:
            # Simulate work with a shared resource
            print(f"Worker thread is working with value: {value}")
            self.resultReady.emit(value)
        finally:
            # Always unlock the mutex
            self.mutex.unlock()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

        # Create a mutex
        self.mutex = QMutex()

        # Create worker threads
        self.worker1 = Worker(self.mutex)
        self.worker2 = Worker(self.mutex)

        # Connect worker signals to slots
        self.worker1.resultReady.connect(self.handle_result)
        self.worker2.resultReady.connect(self.handle_result)

        # Start the worker threads
        self.worker1.start()
        self.worker2.start()

    def initUI(self):
        self.setWindowTitle("QMutex Example")

        layout = QVBoxLayout()

        self.label = QLabel('Result: ')
        layout.addWidget(self.label)

        self.setLayout(layout)

    @pyqtSlot(int)
    def handle_result(self, result):
        # Handle the result from the worker thread
        self.label.setText(f'Result: {result}')

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
