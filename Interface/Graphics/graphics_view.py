from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtGui import QPen, QMouseEvent
from PyQt5.QtCore import Qt, QEvent, QPointF

from Interface.Graphics.scene import GraphicsScene
from Interface.Geometry.point import Point
from Interface.Geometry.line import Line
from Interface.Geometry.pen import Pen


class GraphicsView(QGraphicsView):
    """
    Класс для отображения геометрии
    """

    def __init__(self, tree_model):
        super(GraphicsView, self).__init__()
        self.tree = tree_model

        # self.geometry_tree_element = self.tree.rootItem.childItems[0]

        self.black_pen = QPen(Qt.black)
        self.black_pen.setWidth(3)

        self._zoom = 0
        self.setDragMode(self.ScrollHandDrag)
        self.viewport().setCursor(Qt.ArrowCursor)

        self.graph_scene = GraphicsScene()
        self.graph_scene.setObjectName("graphicsScene")
        self.setScene(self.graph_scene)

        self.init_delta_x = 10
        self.init_delta_y = 100
        self.coef_scale = 10

        self.last_point = None
        self.points_set = set()

        # self.axis_x = Line(self.init_delta_x, self.init_delta_y,
        #               1000 + self.init_delta_x, self.init_delta_y)
        # self.axis_x.setPen(Line.get_pen_axis())
        # print(self.axis_x.line().dx())

        # axis_y = Line(-self.init_delta_x, -self.init_delta_y,
        #               -self.init_delta_x, 100 - self.init_delta_y)
        # axis_y.setPen(Line.get_pen_axis())

        # self.graph_scene.addItem(self.axis_x)
        # self.graph_scene.addItem(axis_y)

        self.add_axis_line('x')
        self.add_axis_line('y')

        self.reset_fit()

    def reset_fit(self):
        """Поворачиваю систему координат"""
        r = self.graph_scene.itemsBoundingRect()
        self.resetTransform()
        self.setSceneRect(r)
        self.fitInView(r, Qt.KeepAspectRatio)
        self.scale(1, -1)

    def add_axis_line(self, flag='x', len_axis_x=1000, len_axis_y=100):
        if flag == 'x':
            self.axis_x = Line(0, self.init_delta_y,
                               len_axis_x + self.init_delta_x * 2.5, self.init_delta_y,
                               'Ось X', self.tree)
            # self.axis_x.setPen(Line.get_pen_axis())
            self.axis_x.setPen(Pen(witdh=2, brush=Qt.darkGray, style=Qt.DashDotLine))
            self.graph_scene.addItem(self.axis_x)
        else:
            self.axis_y = Line(self.init_delta_x, self.init_delta_y,
                               self.init_delta_x, len_axis_y + self.init_delta_y,
                               'Ось X', self.tree)
            # self.axis_y.setPen(Line.get_pen_axis())
            self.axis_y.setPen(Pen(witdh=2, brush=Qt.darkGray, style=Qt.DashDotLine))
            self.graph_scene.addItem(self.axis_y)

    def add_line_to_scene(self, x1, y1, x2, y2, count):
        """Добавляю линию на сцену"""
        x1 = x1 * self.coef_scale + self.init_delta_x
        y1 = y1 * self.coef_scale + self.init_delta_y
        x2 = x2 * self.coef_scale + self.init_delta_x
        y2 = y2 * self.coef_scale + self.init_delta_y
        # x1 += self.init_delta_x
        # y1 += self.init_delta_y
        # x2 += self.init_delta_x
        # y2 += self.init_delta_y

        point_1 = None
        point_2 = None

        flag_was_point_1 = False
        flag_was_point_2 = False

        if self.points_set:
            for point in self.points_set:
                if x1 == point.x and y1 == point.y:
                    point_1 = point
                    flag_was_point_1 = True
                    continue
                elif x2 == point.x and y2 == point.y:
                    point_2 = point
                    flag_was_point_2 = True
                    continue
            if not point_1:
                point_1 = Point(x1, y1, self.last_point.count + 1, self.tree, self.init_delta_x,
                                self.init_delta_y, self.coef_scale)
                self.points_set.add(point_1)
                self.last_point = point_1
            if not point_2:
                point_2 = Point(x2, y2, self.last_point.count + 1, self.tree, self.init_delta_x,
                                self.init_delta_y, self.coef_scale)
                self.points_set.add(point_2)
                self.last_point = point_2
                # else:
                #     point_1 = Point(x1, y1, self.last_point.count + 1)
        else:
            point_1 = Point(x1, y1, count, self.tree, self.init_delta_x,
                            self.init_delta_y, self.coef_scale)
            point_2 = Point(x2, y2, count + 1, self.tree, self.init_delta_x,
                            self.init_delta_y, self.coef_scale)
            self.points_set.add(point_1)
            self.points_set.add(point_2)
            self.last_point = point_2

        # point_2 = Point(x2, y2, point_1.count + 1)
        # self.last_point = point_2

        # self.points_set.add(point_1)
        # self.points_set.add(point_2)

        point_1.log.hovered.connect(self.hoverChange)
        point_1.log.notHovered.connect(self.notHoverChange)

        point_2.log.hovered.connect(self.hoverChange)
        point_2.log.notHovered.connect(self.notHoverChange)

        line = Line(x1, y1, x2, y2, f'Линия {count}', self.tree, self.coef_scale)

        # line.setPen(Line.get_pen_solid())
        line.setPen(Pen(witdh=3, brush=Qt.black, style=Qt.SolidLine))

        if x2 > self.axis_x.line().dx():
            self.graph_scene.removeItem(self.axis_x)
            self.add_axis_line('x', len_axis_x=x2)

        self.tree.insertRows([[line.name, line], [f'Длина - {round(line.len/self.coef_scale, 4)}']],
                             el='line', parent=self.tree.index(0, 0))

        line_index = self.tree.index(count-1, 0, self.tree.index(0, 0))

        self.tree.insertRows([[point_1.name, point_1], [f'x - {round((point_1.x - self.init_delta_x)/self.coef_scale, 4)}, '
                                                        f'y - {round((point_1.y - self.init_delta_y)/self.coef_scale, 4)}']],
                             el='points', parent=line_index)

        self.tree.insertRows([[point_2.name, point_2], [f'x - {round((point_2.x - self.init_delta_x)/self.coef_scale, 4)}, '
                                                        f'y - {round((point_2.y - self.init_delta_y)/self.coef_scale, 4)}']],
                             el='points', parent=line_index)

        self.graph_scene.addItem(line)

        if flag_was_point_1 and flag_was_point_2:
            self.graph_scene.removeItem(point_1)
            self.graph_scene.removeItem(point_2)
            self.graph_scene.addItem(point_1)
            self.graph_scene.addItem(point_2)
        elif flag_was_point_1:
            self.graph_scene.removeItem(point_1)
            self.graph_scene.addItem(point_1)
            self.graph_scene.addItem(point_2)
        elif flag_was_point_2:
            self.graph_scene.removeItem(point_2)
            self.graph_scene.addItem(point_2)
            self.graph_scene.addItem(point_1)
        else:
            self.graph_scene.addItem(point_1)
            self.graph_scene.addItem(point_2)

    def wheelEvent(self, event):
        """Метод для приближения/отдаления на колёсико мыши"""
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

    def mousePressEvent(self, event):
        """Метод определяет действие при зажатых кнопках мыши"""
        if event.button() == Qt.LeftButton:
            self.viewport().setCursor(Qt.ArrowCursor)
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

        super(GraphicsView, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """Метод определяет действие при отпускании кнопкок мыши"""
        if event.button() == Qt.LeftButton:
            self.viewport().setCursor(Qt.ArrowCursor)
            return
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
            self.viewport().setCursor(Qt.ArrowCursor)
        super(GraphicsView, self).mouseReleaseEvent(event)

    def hoverChange(self):
        self.viewport().setCursor(Qt.PointingHandCursor)

    def notHoverChange(self):
        self.viewport().setCursor(Qt.ArrowCursor)
