import sys
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QDrag
from PyQt6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget


class SourceWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.table = QTableWidget(3, 3, self)
        self.table.setHorizontalHeaderLabels(['Column 1', 'Column 2', 'Column 3'])
        
        # Add some items to the table
        for i in range(3):
            for j in range(3):
                item = QTableWidgetItem(f'Item {i+1},{j+1}')
                self.table.setItem(i, j, item)
        
        # Enable drag and drop
        self.table.setDragEnabled(True)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)

        self.setWindowTitle('Source Table')
        self.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.startDrag()

    def startDrag(self):
        selected_items = self.table.selectedItems()
        if selected_items:
            drag = QDrag(self.table)
            mime_data = QMimeData()
            
            # Serialize row data as text, with items separated by a tab character
            row_data = "\t".join([item.text() for item in selected_items])
            mime_data.setText(row_data)
            
            drag.setMimeData(mime_data)
            drag.exec_(Qt.CopyAction | Qt.MoveAction)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    source_window = SourceWindow()
    sys.exit(app.exec_())
