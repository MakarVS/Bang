from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from math import sqrt


class LogObject(QObject):
    hovered = pyqtSignal()
    notHovered = pyqtSignal()


class Point(QGraphicsRectItem):
    def __init__(self, x, y, name):
        super(Point, self).__init__(QRectF(0, 0, 30, 30))
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.name = name
        self.setBrush(QBrush(Qt.black))
        self.setAcceptHoverEvents(True)
        self.log = LogObject()
        self.setPos(x, y)

    def itemChange(self, change, value):
        if change == self.ItemSelectedChange:
            self.setBrush(QBrush(Qt.green) if value else QBrush(Qt.black))
        return QGraphicsItem.itemChange(self, change, value)

    def hoverEnterEvent(self, event):
        self.setBrush(QColor("red"))
        self.log.hovered.emit()
        QGraphicsItem.hoverMoveEvent(self, event)

    def hoverLeaveEvent(self, event):
        self.setBrush(QColor("black"))
        self.log.notHovered.emit()
        QGraphicsItem.hoverMoveEvent(self, event)

    def mousePressEvent(self, event):
        print(self.name)
        QGraphicsItem.mousePressEvent(self, event)


class Viewer(QGraphicsView):
    photoClicked = pyqtSignal(QPoint)
    rectChanged = pyqtSignal(QRect)

    def __init__(self, parent):
        super(Viewer, self).__init__(parent)
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        # self.setMouseTracking(True)
        self.origin = QPoint()
        self.changeRubberBand = False

        self._zoom = 0
        self._empty = True
        self.setScene(QGraphicsScene(self))

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFrameShape(QFrame.NoFrame)
        self.area = float()
        self.setPoints()
        # self.viewport().setCursor(Qt.ArrowCursor)
        QTimer.singleShot(0, self.reset_fit)

    def setItems(self):
        self.data = {
            "x": [
                -2414943.8686,
                -2417160.6592,
                -2417160.6592,
                -2417856.1783,
                -2417054.7618,
                -2416009.9966,
                -2416012.5232,
                -2418160.8952,
                -2418160.8952,
                -2416012.5232,
                -2417094.7694,
                -2417094.7694,
            ],
            "y": [
                10454269.7008,
                10454147.2672,
                10454147.2672,
                10453285.2456,
                10452556.8132,
                10453240.2808,
                10455255.8752,
                10455183.1912,
                10455183.1912,
                10455255.8752,
                10456212.5959,
                10456212.5959,
            ],
        }
        maxX = max(self.data["x"])
        minX = min(self.data["x"])
        maxY = max(self.data["y"])
        minY = min(self.data["y"])
        distance = sqrt((maxX - minX) ** 2 + (maxY - minY) ** 2)

        self.area = QRectF(minX, minY, distance, distance)
        self.scene().setSceneRect(
            QRectF(minX, -minY, distance, distance)
        )  # Tried this but didn't seem to do anything
        for i, (x, y) in enumerate(zip(self.data["x"], self.data["y"])):
            p = Point(x, y, "Point__" + str(i))
            p.log.hovered.connect(self.hoverChange)
            p.log.notHovered.connect(self.notHoverChange)
            self.scene().addItem(p)

    def setPoints(self):
        self.setItems()
        self.setDragMode(self.ScrollHandDrag)

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            factor = 1.25
            self._zoom += 1
        else:
            factor = 0.8

            self._zoom -= 1
        if self._zoom > 0:
            self.scale(factor, factor)
        elif self._zoom == 0:
            self.reset_fit()
        else:
            self._zoom = 0

    def hoverChange(self):
        self.viewport().setCursor(Qt.PointingHandCursor)

    def notHoverChange(self):
        self.viewport().setCursor(Qt.ArrowCursor)

    def mousePressEvent(self, event):
        # if event.button() == Qt.LeftButton:
        #     self.viewport().setCursor(Qt.ArrowCursor)
        #     return
        if event.button() == Qt.LeftButton:
            self.origin = event.pos()
            self.rubberBand.setGeometry(QRect(self.origin, QSize()))
            self.rectChanged.emit(self.rubberBand.geometry())
            self.rubberBand.show()
            self.changeRubberBand = True
            return

        elif event.button() == Qt.MidButton:
            self.viewport().setCursor(Qt.ClosedHandCursor)
            self.original_event = event
            handmade_event = QMouseEvent(
                QEvent.MouseButtonPress,
                QPointF(event.pos()),
                Qt.LeftButton,
                event.buttons(),
                Qt.KeyboardModifiers(),
            )
            QGraphicsView.mousePressEvent(self, handmade_event)

        super(Viewer, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        point = event.pos()
        print(self.mapToScene(point))
        # if event.button() == Qt.LeftButton:
        #     self.viewport().setCursor(Qt.ArrowCursor)
        #     return
        if event.button() == Qt.LeftButton:
            self.changeRubberBand = False
            if self.rubberBand.isVisible():
                self.rubberBand.hide()
                rect = self.rubberBand.geometry()
                rect_scene = self.mapToScene(rect).boundingRect()
                selected = self.scene().items(rect_scene)
                if selected:
                    print(
                        "".join("Item: %s\n" % child.name for child in selected)
                    )
                else:
                    print(" Nothing\n")
            QGraphicsView.mouseReleaseEvent(self, event)

        elif event.button() == Qt.MidButton:
            self.viewport().setCursor(Qt.ArrowCursor)
            handmade_event = QMouseEvent(
                QEvent.MouseButtonRelease,
                QPointF(event.pos()),
                Qt.LeftButton,
                event.buttons(),
                Qt.KeyboardModifiers(),
            )
            QGraphicsView.mouseReleaseEvent(self, handmade_event)
        super(Viewer, self).mouseReleaseEvent(event)

    # def mouseMoveEvent(self, event):
    #     if self.changeRubberBand:
    #         self.rubberBand.setGeometry(
    #             QRect(self.origin, event.pos()).normalized()
    #         )
    #         self.rectChanged.emit(self.rubberBand.geometry())
    #         QGraphicsView.mouseMoveEvent(self, event)
    #     super(Viewer, self).mouseMoveEvent(event)

    def hoverMoveEvent(self, event):
        point = event.pos().toPoint()
        print(point)
        QGraphicsView.hoverMoveEvent(event)

    def reset_fit(self):
        r = self.scene().itemsBoundingRect()
        self.resetTransform()
        self.setSceneRect(r)
        self.fitInView(r, Qt.KeepAspectRatio)
        self._zoom = 0
        self.scale(1, -1)


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.viewer = Viewer(self)
        # self.btnLoad = QToolButton(self)
        # self.btnLoad.setText("Fit Into View")
        # self.btnLoad.clicked.connect(self.fitPoints)

        VBlayout = QVBoxLayout(self)
        VBlayout.addWidget(self.viewer)
        # HBlayout = QHBoxLayout()
        # HBlayout.setAlignment(Qt.AlignLeft)
        # HBlayout.addWidget(self.btnLoad)
        #
        # VBlayout.addLayout(HBlayout)

    def fitPoints(self):
        self.viewer.reset_fit()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = Window()
    window.setGeometry(500, 300, 800, 600)
    window.show()
    sys.exit(app.exec_())