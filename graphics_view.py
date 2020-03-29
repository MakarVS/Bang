import sys

from PyQt5.QtWidgets import QWidget, QGraphicsView


class GraphicView(QWidget):
    def __init__(self):
        self.graphics = QGraphicsView()
        self.graphicsView.setObjectName("graphicsView")
