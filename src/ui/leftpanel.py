from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem

class LeftPanel(QTreeWidget):
    def __init__(self, parent=None):
        super(LeftPanel, self).__init__(parent)
        self.setHeaderLabels(["Tree Widget"])
        for i in range(5):
            item = QTreeWidgetItem([f"Item {i}"])
            self.addTopLevelItem(item)