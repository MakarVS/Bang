from PyQt5.QtWidgets import QWidget, QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QPen
from PyQt5.QtCore import Qt
from PyQt5.Qt import QLineF


class GraphicsView(QGraphicsView):
    """
    Класс для отображения геометрии
    """

    def __init__(self):
        super(GraphicsView, self).__init__()
        self.black_pen = QPen(Qt.black)
        self.black_pen.setWidth(3)

        self.graph_scene = QGraphicsScene()
        self.graph_scene.setObjectName("graphicsScene")
        self.graph_scene.setSceneRect(Qt.QRectF())

        self.setScene(self.graph_scene)

        # self.graph_view = QGraphicsView(self.graph_scene, self)
        # self.graph_view.setObjectName("graphicsView")
        # self.graph_view.translate()
        point_1 = self.graph_view.mapFromScene(0, 0)
        point_2 = self.graph_view.mapFromScene(100, 100)

        self.graph_scene.addLine(0, 0, 200, 200)

        self.graph_view.show()
        # self.graph_view.
