from PyQt5.QtCore import QAbstractItemModel
from PyQt5.QtCore import Qt, QModelIndex


class TreeItem(object):
    def __init__(self, data, parent=None):
        self.parentItem = parent
        self.itemData = data
        self.childItems = []

    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        try:
            return self.childItems[row]
        except IndexError:
            return None

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return len(self.itemData)

    def data(self, column):
        try:
            return self.itemData[column]
        except IndexError:
            return None

    def parent(self):
        return self.parentItem

    def childNumber(self):
        if self.parentItem != None:
            return self.parentItem.childItems.index(self)
        return 0

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)

        return 0

    def insertChildren(self, data, position, count):
        if position < 0 or position > len(self.childItems):
            return False

        for row in range(count):
            item = TreeItem(data, self)
            self.childItems.insert(position, item)

        return True


class TreeModel(QAbstractItemModel):
    def __init__(self, view, data=None, parent=None):
        super(TreeModel, self).__init__(parent)
        self.rootItem = TreeItem(['Процесс', 'Описание'])

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.rootItem.data(section)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    def columnCount(self, parent=QModelIndex()):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def getItem(self, index):
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item

        return self.rootItem

    def index(self, row, column, parent=QModelIndex()):
        if parent.isValid() and parent.column() != 0:
            return QModelIndex()

        parentItem = self.getItem(parent)
        childItem = parentItem.child(row)

        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = self.getItem(index)
        a = (childItem.itemData)
        parentItem = childItem.parent()
        b = (parentItem.itemData)

        if parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.childNumber(), 0, parentItem)

    def data(self, index, role):
        if not index.isValid():
            return None

        if role != Qt.DisplayRole and role != Qt.EditRole:
            return None

        item = self.getItem(index)
        return item.data(index.column())[0]

    def setData(self, left_index, right_index, role=Qt.EditRole):
        if role != Qt.EditRole:
            return False

        self.dataChanged.emit(left_index, right_index, [Qt.DisplayRole])

        return True

    def insertRows(self, data, el=None, parent=QModelIndex()):
        parentItem = self.getItem(parent)
        position = len(parentItem.childItems)

        self.beginInsertRows(parent, position, 1)
        success = parentItem.insertChildren(data, position, 1)
        self.endInsertRows()

        if el == 'line':
            # init_index = self.index(0, 0, self.index(0, 0))
            # current_index = self.index(position, 0, self.index(0, 0))
            # print(self.getItem(current_index).itemData)
            self.setData(self.index(0, 0), self.index(0, 0))
        elif el == 'points':
            current_index = self.index(position, 0, self.index(0, 0))
            self.setData(current_index, current_index)
        # elif el == 'points_2':
        #     current_index = self.index(1, 0, self.index(0, 0))
        #     self.setData(current_index, current_index)

        return success


