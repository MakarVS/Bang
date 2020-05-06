from PyQt5.QtWidgets import QWidget, QGraphicsScene
from PyQt5.QtGui import QPen
from PyQt5.QtCore import Qt


class GraphicsScene(QGraphicsScene):
    """
    """

    def __init__(self):
        super(GraphicsScene, self).__init__()

    def drawBackground(self, painter, rec):
        painter.setPen(QPen(Qt.red, 3))
        # painter.drawRect(self.sceneRect())
