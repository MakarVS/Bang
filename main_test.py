import sys

from PyQt5 import QtWidgets, QtCore
import sip

from icons import icon
from message_box import MessageBox
from geometry import GeometryWindow
from graphics_view import GraphicView
from tree import Tree


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        self.setObjectName("MainWindow")

        self.centralwidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralwidget)
        self.message = MessageBox()

        self.grid_geometry = QtWidgets.QGridLayout(self.centralwidget)
        self.grid_geometry.setObjectName("grid_geometry")

        self._translate = QtCore.QCoreApplication.translate

        self.widget_geometry = None
        self.statusbar = None

        self.create_actions_menubar()
        self.create_actions_toolbar()
        self.create_menubar()
        self.create_toolbar()
        self.change_statusbar()

    def create_menubar(self,):
        self.menubar = QtWidgets.QMenuBar(self.centralwidget)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1440, 21))
        self.menubar.setObjectName("menubar")

        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu.setTitle(self._translate("MainWindow", "Файл"))
        self.menu.addAction(self.action_new_file)
        self.menu.addAction(self.action_close_file)

        self.setMenuBar(self.menubar)
        self.menubar.addAction(self.menu.menuAction())

    def create_toolbar(self):
        self.toolBar = QtWidgets.QToolBar(self.centralwidget)
        self.toolBar.setObjectName("toolbar")
        self.toolBar.addAction(self.action_geometry)
        self.toolBar.addSeparator()

        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)

    def change_statusbar(self, text='Пусто'):
        if not self.statusbar:
            self.statusbar = QtWidgets.QStatusBar(self.centralwidget)
            self.statusbar.setObjectName("statusbar")
            self.setStatusBar(self.statusbar)

        self.statusbar.showMessage(text)

    def create_actions_menubar(self):
        self.action_new_file = QtWidgets.QAction(self.centralwidget,
                                                 triggered=self.create_new_calc)
        self.action_new_file.setIcon(icon('./icon/new_file.png'))
        self.action_new_file.setObjectName("action_new_file")
        self.action_new_file.setText(self._translate("MainWindow", "Новый расчет"))

        self.action_close_file = QtWidgets.QAction(self.centralwidget,
                                                 triggered=self.close_calc)
        self.action_close_file.setIcon(icon('./icon/close_file.png'))
        self.action_close_file.setObjectName("action_close_file")
        self.action_close_file.setText(self._translate("MainWindow", "Закрыть расчет"))

    def create_actions_toolbar(self):
        self.action_geometry = QtWidgets.QAction(self.centralwidget,
                                                 triggered=self.create_geometry_interface)
        self.action_geometry.setEnabled(False)
        self.action_geometry.setCheckable(True)
        self.action_geometry.setIcon(icon('./icon/geometry.png'))
        self.action_geometry.setShortcut('Ctrl+G')
        self.action_geometry.setIconText('Геометрия Ctrl+G')

    def create_new_calc(self):
            # self.message.save()
        self.action_geometry.setEnabled(True)
        self.change_statusbar('Новый расчёт')

    def create_geometry_interface(self):
        if self.widget_geometry:
            self.widget_geometry.show()
        else:
            geometry = GeometryWindow()
            self.widget_geometry = geometry.widget_geometry
            self.grid_geometry.addWidget(self.widget_geometry, 0, 0, 1, 1)

        self.change_statusbar('Геометрия')
        self.action_geometry.setEnabled(False)

    def close_calc(self):
        if self.widget_geometry:
            sip.delete(self.widget_geometry)
            self.action_geometry.setChecked(False)
            self.widget_geometry = None
            self.change_statusbar()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle('Pif-paf')
    window.resize(1440, 942)
    window.show()
    sys.exit(app.exec_())


