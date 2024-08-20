from PyQt6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QColor

app = QApplication([])

# Create a QTableWidget instance
table = QTableWidget(5, 3)  # 5 rows, 3 columns

# Populate the table with some data
for row in range(5):
    for col in range(3):
        table.setItem(row, col, QTableWidgetItem(f"Item {row}, {col}"))

# Apply the custom stylesheet
table.setStyleSheet("""
    QTableWidget {
        border: 1px solid white; /* Border around the table */
        color: #ffffff;
    }
    QHeaderView::section {
        background-color: #232629; /* Header background color */
        border: 1px solid white;   /* Border around headers */
        padding: 4px;
    }
    QTableWidget::item {
        background-color: #31363b; /* Cell background color */
        border: 1px solid white;   /* Border around cells */
    }
    QScrollBar:vertical {
        border: 1px solid white;
        background: #31363b;
        width: 10px;
    }
    QScrollBar::handle:vertical {
        background: #232629;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        border: 1px solid white;
        background: #31363b;
    }
    QScrollBar:horizontal {
        border: 1px solid white;
        background: #31363b;
        height: 10px;
    }
    QScrollBar::handle:horizontal {
        background: #232629;
    }
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
        border: 1px solid white;
        background: #31363b;
    }
""")

# Show the table
table.show()

# Run the application
app.exec_()