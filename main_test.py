import sys

from PyQt5 import QtWidgets, QtCore

from icons import icon


class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        self.setObjectName("MainWindow")

        self._translate = QtCore.QCoreApplication.translate

        self.create_actions()
        self.create_menubar()

    def create_menubar(self,):
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1693, 21))
        self.menubar.setObjectName("menubar")

        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu.setTitle(self._translate("MainWindow", "Файл"))
        self.menu.addAction(self.action_new_file)

        self.menubar.addAction(self.menu.menuAction())

    def create_actions(self):
        self.action_new_file = QtWidgets.QAction(self, triggered=self.create_new_calc)
        self.action_new_file.setIcon(icon('./icon/new_file.png'))
        self.action_new_file.setObjectName("action_new_file")
        self.action_new_file.setText(self._translate("MainWindow", "Новый расчет"))

    def create_new_calc(self):
        print('asd')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle('Pif-paf')
    window.resize(1000, 500)
    window.show()
    sys.exit(app.exec_())


