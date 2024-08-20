import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget


class DestinationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.table = QTableWidget(0, 3, self)  # Start with 0 rows
        self.table.setHorizontalHeaderLabels(['Column 1', 'Column 2', 'Column 3'])
        
        # Enable drop
        self.table.setAcceptDrops(True)
        
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.setWindowTitle('Destination Table')
        self.show()

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        row_data = event.mimeData().text().split('\t')
        
        # Insert a new row at the end
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        # Populate the new row with the dropped data
        for column, data in enumerate(row_data):
            new_item = QTableWidgetItem(data)
            self.table.setItem(row_position, column, new_item)

        event.acceptProposedAction()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    destination_window = DestinationWindow()
    sys.exit(app.exec_())
