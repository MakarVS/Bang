from PyQt5 import QtWidgets, QtCore
import sip

from icons import icon
from message_box import MessageBox
from Interface.Geometry.geometry import GeometryWindow
from Interface.Graphics.graphics_view import GraphicsView
from Interface.Tree.tree_view import TreeView
from Interface.Tree.tree_model import TreeModel
from Interface.Calculation.calc_base import CalculationWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()

        self.setObjectName("MainWindow")

        self.centralwidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralwidget)

        self.message = MessageBox()

        self.grid_central = QtWidgets.QGridLayout(self.centralwidget)
        self.grid_central.setObjectName("grid_central")

        self._translate = QtCore.QCoreApplication.translate

        self.visible_geom = None
        self.visible_calc = None
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
        self.toolBar.addAction(self.action_calculation)

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

        self.action_calculation = QtWidgets.QAction(self.centralwidget,
                                                    triggered=self.create_calculation_interface)
        self.action_calculation.setEnabled(False)
        self.action_calculation.setCheckable(True)
        self.action_calculation.setIcon(icon('./icon/shoot.png'))
        self.action_calculation.setShortcut('Ctrl+C')
        self.action_calculation.setIconText('Расчет Ctrl+C')

    def create_new_calc(self):
            # self.message.save()
        self.action_geometry.setEnabled(True)
        self.action_calculation.setEnabled(False)
        self.change_statusbar('Новый расчёт')

    def create_geometry_interface(self):
        if self.visible_geom:
            self.geometry.tabWidget.show()
            self.calculation.tabWidget.hide()
            self.action_calculation.setEnabled(True)
            self.action_calculation.setChecked(False)
        else:
            self.tree_view = TreeView()
            self.tree_model = TreeModel(self.tree_view)
            self.tree_view.setModel(self.tree_model)
            # self.tree_model.insertRows([['Геометрия', self.geometry], ['Построение геометрии ствола']])
            self.tree_view.click()
            # self.tree_view.selectionModel().setCurrentIndex(self.tree_model.index(0, 0, a))
            self.graphics = GraphicsView(self.tree_model)

            self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
            self.horizontalLayout = QtWidgets.QHBoxLayout()
            self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
            self.horizontalLayout.setContentsMargins(0, -1, -1, -1)
            self.horizontalLayout.setSpacing(50)
            self.horizontalLayout.setObjectName("horizontalLayout")
            self.geometry = GeometryWindow(self, self.centralwidget, self.tree_view, self.graphics)
            self.tree_model.insertRows([['Геометрия', self.geometry], ['Построение геометрии ствола']])
            self.calculation = CalculationWindow(self, self.centralwidget, self.tree_view, self.graphics)

            self.horizontalLayout.addWidget(self.geometry.tabWidget)
            self.horizontalLayout.addWidget(self.calculation.tabWidget)
            self.calculation.tabWidget.hide()
            self.horizontalLayout.addWidget(self.tree_view)
            self.horizontalLayout.setStretch(0, 2)
            self.horizontalLayout.setStretch(1, 2)
            self.horizontalLayout.setStretch(2, 1)

            self.grid_central.addLayout(self.horizontalLayout, 1, 0, 1, 1)
            self.grid_central.addWidget(self.graphics, 0, 0, 1, 1)

            self.grid_central.setRowStretch(0, 1)
            self.grid_central.setRowStretch(1, 1)

            self.action_calculation.setEnabled(False)
            self.visible_geom = True

        self.change_statusbar('Геометрия')
        self.action_geometry.setEnabled(False)

    def create_calculation_interface(self):
        if self.visible_calc:
            self.geometry.tabWidget.hide()
            self.calculation.tabWidget.show()
        else:
            self.tree_model.insertRows([['Расчет', self.calculation], ['Задание параметров расчета']])

            self.geometry.tabWidget.hide()
            self.calculation.tabWidget.show()

            self.visible_calc = True

        self.change_statusbar('Расчет')
        self.action_calculation.setEnabled(False)
        self.action_geometry.setEnabled(True)
        self.action_geometry.setChecked(False)

    def close_calc(self):
        if self.calculation or self.geometry:
            sip.delete(self.graphics)
            sip.delete(self.tree)
            sip.delete(self.geometry)
            sip.delete(self.calculation)
            sip.delete(self.grid_central)
            self.action_geometry.setChecked(False)
            self.action_calculation.setChecked(False)
            self.visible_geom = None
            self.visible_calc = None
            self.change_statusbar()
