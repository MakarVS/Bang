from PyQt5.QtWidgets import QWidget, QTreeWidget


class Tree(QWidget):
    def __init__(self):
        self.treeWidget = QTreeWidget()
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
