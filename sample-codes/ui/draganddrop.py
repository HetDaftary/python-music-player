from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

class MyTableWidget(QTableWidget):
    def __init__(self, rows, columns, parent=None):
        super().__init__(rows, columns, parent)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(QTableWidget.InternalMove)
        self.setSelectionBehavior(QTableWidget.SelectRows)

    def dragEnterEvent(self, event):
        if event.source() == self:
            event.setDropAction(Qt.MoveAction)
        else:
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        source_table = event.source()
        if source_table == self:
            super().dropEvent(event)
        else:
            # Assuming we're dropping a row from another table
            row = source_table.currentRow()
            new_row_position = self.rowCount()
            self.insertRow(new_row_position)

            for column in range(source_table.columnCount()):
                item = source_table.item(row, column)
                if item:
                    new_item = QTableWidgetItem(item.text())
                    self.setItem(new_row_position, column, new_item)

            source_table.removeRow(row)

            event.setDropAction(Qt.MoveAction)
            event.accept()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Drag and Drop Between Tables")

        self.table1 = MyTableWidget(3, 3)
        self.table2 = MyTableWidget(3, 3)

        # Fill the first table with some items
        for row in range(3):
            for column in range(3):
                item = QTableWidgetItem(f"Item {row}, {column}")
                self.table1.setItem(row, column, item)

        layout = QVBoxLayout()
        layout.addWidget(self.table1)
        layout.addWidget(self.table2)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

def create_second_window(app):
    second_window = MainWindow()
    second_window.setWindowTitle("Second Window")
    second_window.show()
    return second_window

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window1 = MainWindow()
    window1.show()

    # Create the second window
    window2 = create_second_window(app)

    sys.exit(app.exec_())
