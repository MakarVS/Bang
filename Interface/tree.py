from PyQt5.QtWidgets import QWidget, QTreeWidget


class TreeWindow(QWidget):
    def __init__(self):
        super(TreeWindow, self).__init__()
        self.treeWidget = QTreeWidget()
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
