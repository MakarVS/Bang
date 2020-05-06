from PyQt5.QtWidgets import QTreeView, QAbstractItemView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush

from Interface.Geometry.pen import Pen
import Interface


class TreeView(QTreeView):
    def __init__(self):
        super(QTreeView, self).__init__()
        self.setObjectName("treeWidget")
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.flag_selected = False

    def click(self):
        self.clicked.connect(self.select_geometry)

    def select_geometry(self, index):
        if self.flag_selected:
            if self.last_select_type == Interface.Geometry.line.Line:
                self.last_select.setPen(Pen(witdh=3, brush=Qt.black, style=Qt.SolidLine))
                current_item = self.model().getItem(index).itemData[0][1]
                buf_type = type(current_item)
                if buf_type == Interface.Geometry.line.Line or buf_type == Interface.Geometry.point.Point:
                    self.last_select = current_item
                    self.last_select.setPen(Pen(witdh=3, brush=Qt.red, style=Qt.SolidLine))
            elif self.last_select_type == Interface.Geometry.point.Point:
                self.last_select.setBrush(QBrush(Qt.black))
                current_item = self.model().getItem(index).itemData[0][1]
                buf_type = type(current_item)
                if buf_type == Interface.Geometry.line.Line or buf_type == Interface.Geometry.point.Point:
                    self.last_select = current_item
                    self.last_select.setBrush(QBrush(Qt.red))
        else:
            self.last_select = self.model().getItem(index).itemData[0][1]
            self.last_select_type = type(self.last_select)

            if self.last_select_type == Interface.Geometry.line.Line:
                self.last_select.setPen(Pen(witdh=3, brush=Qt.red, style=Qt.SolidLine))
            elif self.last_select_type == Interface.Geometry.point.Point:
                self.last_select.setBrush(QBrush(Qt.red))

            self.flag_selected = True
