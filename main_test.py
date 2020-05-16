import sys

from PyQt5 import QtWidgets

from Interface.main_interface import MainWindow
from icons import icon


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()

    window.setWindowTitle('Bang')
    window.setWindowIcon(icon('./icon/bang.png'))
    
    window.resize(1440, 942)
    window.show()
    sys.exit(app.exec_())
