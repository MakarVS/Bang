from PyQt5.QtWidgets import QWidget, QMessageBox


class MessageBox(QWidget):
    def save(self):
        save = QMessageBox()
        save.setWindowTitle('Сохранение')
        save.setText('Вы хотите сохранить проект?')
        save.setIcon(QMessageBox.Question)
        save.standardButtons(QMessageBox.Yes, QMessageBox.No, QMessageBox.Cancel)
        save.setDefaultButton(QMessageBox.Cancel)

        if save.question == QMessageBox.Yes:
            print('Yes')
        # elif save == QMessageBox.No:

