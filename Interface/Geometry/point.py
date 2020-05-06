from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsItem
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import QRectF, Qt

from Interface.logobject import LogObject


class Point(QGraphicsEllipseItem):
    def __init__(self, x, y, count, tree, delta_x, delta_y, coef_scale):
        super(Point, self).__init__(QRectF(0, 0, 5, 5))
        self.tree = tree
        self.count = count
        self.name = f'Точка {count}'
        self.x = x
        self.y = y
        self.setBrush(QBrush(Qt.black))
        self.setAcceptHoverEvents(True)
        self.setToolTip(f'{self.name}: {round((x-delta_x)/coef_scale, 4)}; '
                        f'{round((y-delta_y)/coef_scale, 4)}')

        self.setAcceptHoverEvents(True)
        self.log = LogObject()

        self.flag_points_wall = False
        self.flag_points_geom_barell = False

        self.setPos(x-2.5, y-2.5)

    def hoverEnterEvent(self, event):
        self.setBrush(QBrush(Qt.red))
        self.log.hovered.emit()
        QGraphicsItem.hoverMoveEvent(self, event)

    def hoverLeaveEvent(self, event):
        self.setBrush(QBrush(Qt.black))
        self.log.notHovered.emit()
        QGraphicsItem.hoverMoveEvent(self, event)

    def mousePressEvent(self, event):
        if self.flag_points_wall:
            if event.button() == Qt.LeftButton:
                calc = self.tree.rootItem.childItems[1].itemData[0][1]
                text = calc.lineEdit_points_wall.text()
                if text:
                    if self.name not in text:
                        calc.lineEdit_points_wall.setText(f'{text}, {self.name}')
                        calc.points_wall_list.append(self)
                else:
                    calc.lineEdit_points_wall.setText(self.name)
                    calc.points_wall_list.append(self)
            QGraphicsItem.mousePressEvent(self, event)
        elif self.flag_points_geom_barell:
            if event.button() == Qt.LeftButton:
                calc = self.tree.rootItem.childItems[1].itemData[0][1]
                text = calc.lineEdit_points_geom_barell.text()
                if text:
                    if self.name not in text:
                        calc.lineEdit_points_geom_barell.setText(f'{text}, {self.name}')
                        calc.points_geom_barell_list.append(self)
                else:
                    calc.lineEdit_points_geom_barell.setText(self.name)
                    calc.points_geom_barell_list.append(self)
            QGraphicsItem.mousePressEvent(self, event)
