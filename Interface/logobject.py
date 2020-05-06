from PyQt5.QtCore import QObject, pyqtSignal


class LogObject(QObject):
    hovered = pyqtSignal()
    notHovered = pyqtSignal()
