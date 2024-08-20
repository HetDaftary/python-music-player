import sys
from PyQt6.QtWidgets import QApplication, QHeaderView, QMainWindow, QTreeWidget, QTableWidget, QTreeWidgetItem, QTableWidgetItem, QHBoxLayout, QWidget, QSplitter
from PyQt6.QtCore import Qt

class TreeWidgetClass(QTreeWidget):
    def __init__(self, parent=None):
        super(TreeWidgetClass, self).__init__(parent)
        self.setHeaderLabels(["Tree Widget"])
        for i in range(5):
            item = QTreeWidgetItem([f"Item {i}"])
            self.addTopLevelItem(item)

class TableWidgetClass(QTableWidget):
    def __init__(self, parent=None):
        super(TableWidgetClass, self).__init__(parent)
        self.setRowCount(10)
        self.setColumnCount(5)

        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for row in range(10):
            for col in range(5):
                self.setItem(row, col, QTableWidgetItem(f"Cell {row},{col}"))

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Tree and Table Widgets Example")
        
        # Create instances of TreeWidgetClass and TableWidgetClass
        self.tree_widget = TreeWidgetClass()
        self.table_widget = TableWidgetClass()

        # Create a splitter to manage the layout
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.addWidget(self.tree_widget)
        self.splitter.addWidget(self.table_widget)

        # Set the stretch factors
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 7)

        # Set the central widget of the main window
        self.setCentralWidget(self.splitter)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
