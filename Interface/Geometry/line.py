from PyQt5.Qt import QGraphicsItem, QGraphicsLineItem, QLineF
from PyQt5.QtCore import Qt

from Interface.logobject import LogObject
from Interface.Geometry.pen import Pen


class Line(QGraphicsLineItem):
    def __init__(self, x1, y1, x2, y2, name, tree, coef_scale=None):
        super(Line, self).__init__()
        self.tree = tree
        line = QLineF(x1, y1, x2, y2)
        self.name = name
        self.len = round(line.length(), 2)
        self.setLine(line)
        self.setAcceptHoverEvents(True)
        self.log = LogObject()

        self.flag_mouse_event = False

        if name in ('Ось X', 'Ось Y'):
            self.setToolTip(f'{name}')
        else:
            self.setToolTip(f'{name}. Длина - {round(self.len/coef_scale, 4)}')

        self.hover_pen = Pen(witdh=3, brush=Qt.red, style=Qt.SolidLine)

    def hoverEnterEvent(self, event):
        self.last_pen = self.pen()
        self.setPen(self.hover_pen)
        self.log.hovered.emit()
        QGraphicsItem.hoverMoveEvent(self, event)

    def hoverLeaveEvent(self, event):
        self.setPen(self.last_pen)
        self.log.notHovered.emit()
        QGraphicsItem.hoverMoveEvent(self, event)

    def mousePressEvent(self, event):
        if self.flag_mouse_event:
            if event.button() == Qt.LeftButton:
                calc = self.tree.rootItem.childItems[1].itemData[0][1]
                calc.border_cam = self
                calc.choose_border_cam_false()
                calc.lineEdit_border_cam.setText(self.name)
            QGraphicsItem.mousePressEvent(self, event)
