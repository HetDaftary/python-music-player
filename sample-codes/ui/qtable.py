import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QMessageBox, QSizePolicy

class TableDemo(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the QTableWidget
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(4)
        self.tableWidget.setColumnCount(3)

        # Set headers
        self.tableWidget.setHorizontalHeaderLabels(['Name', 'Age', 'Occupation'])

        # Add initial items
        self.tableWidget.setItem(0, 0, QTableWidgetItem('Alice'))
        self.tableWidget.setItem(0, 1, QTableWidgetItem('30'))
        self.tableWidget.setItem(0, 2, QTableWidgetItem('Engineer'))
        self.tableWidget.setItem(1, 0, QTableWidgetItem('Bob'))
        self.tableWidget.setItem(1, 1, QTableWidgetItem('25'))
        self.tableWidget.setItem(1, 2, QTableWidgetItem('Designer'))
        self.tableWidget.setItem(2, 0, QTableWidgetItem('Charlie'))
        self.tableWidget.setItem(2, 1, QTableWidgetItem('35'))
        self.tableWidget.setItem(2, 2, QTableWidgetItem('Teacher'))
        self.tableWidget.setItem(3, 0, QTableWidgetItem('Diana'))
        self.tableWidget.setItem(3, 1, QTableWidgetItem('28'))
        self.tableWidget.setItem(3, 2, QTableWidgetItem('Doctor'))

        # Connect cell click signal to a custom slot
        self.tableWidget.cellClicked.connect(self.cell_clicked)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)

        # Add button layout
        button_layout = QHBoxLayout()
        add_button = QPushButton("Add Row")
        remove_button = QPushButton("Remove Row")
        button_layout.addWidget(add_button)
        button_layout.addWidget(remove_button)

        layout.addLayout(button_layout)

        # Connect buttons to slots
        add_button.clicked.connect(self.add_row)
        remove_button.clicked.connect(self.remove_row)

        self.setLayout(layout)
        self.setWindowTitle('QTableWidget Example')

    def cell_clicked(self, row, column):
        item = self.tableWidget.item(row, column)
        if item:
            QMessageBox.information(self, "Cell Clicked", f"Row: {row}, Column: {column}\nContent: {item.text()}")

    def add_row(self):
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)
        self.tableWidget.setItem(row_position, 0, QTableWidgetItem('New Name'))
        self.tableWidget.setItem(row_position, 1, QTableWidgetItem('Age'))
        self.tableWidget.setItem(row_position, 2, QTableWidgetItem('Occupation'))

    def remove_row(self):
        if self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(self.tableWidget.rowCount() - 1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = TableDemo()
    demo.show()
    sys.exit(app.exec_())
