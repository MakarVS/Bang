from PyQt5 import QtGui


def icon(way):
    ic = QtGui.QIcon()
    ic.addPixmap(QtGui.QPixmap(way), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    return ic
