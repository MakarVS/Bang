from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QLayout, QHBoxLayout, QLabel, \
    QLineEdit, QFrame, QSizePolicy, QSpacerItem, QPushButton, QComboBox
from PyQt5.QtCore import Qt, QSize, QCoreApplication


class GeometryWindow(QWidget):
    """
    Класс для создания комплексного окна геометрии, которое открывается по нажатию кнопки "Геометрия"
    """

    def __init__(self, main_window, horizontal, tree, graphics):
        self._translate = QCoreApplication.translate
        super(GeometryWindow, self).__init__()

        self.count_lines = 0

        self.main_window = main_window

        self.get_tab_widget(horizontal)
        self.tree = tree

        self.graphics = graphics

    def get_tab_widget(self, horizontal):
        """
        Создание окна с вкладками для построения геометрии
        :return:
        """
        self.tabWidget = QTabWidget(horizontal)
        self.tabWidget.setStyleSheet("backhround-color:rgb(156, 156, 156)")
        self.tabWidget.setTabPosition(QTabWidget.North)
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.tabWidget.setObjectName("tabWidget")

        self.get_two_points()
        self.tabWidget.addTab(self.two_points, '')
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.two_points),
                                  self._translate("GeometryWindow", "Построение линии по двум точкам"))

    def get_two_points(self):
        """
        Создание первой вкладки для построения геометрии по координатам двух точек
        :return:
        """
        self.two_points = QWidget()
        self.two_points.setObjectName("two_points")

        self.two_points_layout = QVBoxLayout(self.two_points)
        self.two_points_layout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.two_points_layout.setObjectName("two_points_layout")

        self.layout_input_two_points = QHBoxLayout()
        self.layout_input_two_points.setObjectName("layout_input_two_points")

        self.point_1 = QVBoxLayout()
        self.point_1.setObjectName("point_1")

        self.label_point_1 = QLabel(self.two_points)
        self.label_point_1.setTextFormat(Qt.AutoText)
        self.label_point_1.setObjectName("label_point_1")
        self.label_point_1.setText(self._translate("GeometryWindow",
                                                   "<html><head/><body><p><span style=\" font-size:10pt;\">Введите координаты первой точки</span></p></body></html>"))

        self.point_1.addWidget(self.label_point_1)

        self.x1_line = QHBoxLayout()
        self.x1_line.setObjectName("x1_line")
        self.label_x1 = QLabel(self.two_points)
        self.label_x1.setObjectName("label_x1")
        self.label_x1.setText(self._translate("GeometryWindow",
                                              "<html><head/><body><p><span style=\" font-size:10pt;\">x1</span></p></body></html>"))
        self.x1_line.addWidget(self.label_x1)

        self.lineEdit_x1 = QLineEdit(self.two_points)
        self.lineEdit_x1.setMinimumSize(QSize(0, 25))
        self.lineEdit_x1.setFrame(True)
        self.lineEdit_x1.setEchoMode(QLineEdit.Normal)
        self.lineEdit_x1.setDragEnabled(False)
        self.lineEdit_x1.setPlaceholderText("")
        self.lineEdit_x1.setCursorMoveStyle(Qt.LogicalMoveStyle)
        self.lineEdit_x1.setClearButtonEnabled(False)
        self.lineEdit_x1.setObjectName("lineEdit_x1")
        self.lineEdit_x1.setText('0.0')

        self.x1_line.addWidget(self.lineEdit_x1)
        self.point_1.addLayout(self.x1_line)

        self.y1_line = QHBoxLayout()
        self.y1_line.setObjectName("y1_line")

        self.label_y1 = QLabel(self.two_points)
        self.label_y1.setObjectName("label_y1")
        self.label_y1.setText(self._translate("GeometryWindow",
                                              "<html><head/><body><p><span style=\" font-size:10pt;\">y1</span></p></body></html>"))
        self.y1_line.addWidget(self.label_y1)

        self.lineEdit_y1 = QLineEdit(self.two_points)
        self.lineEdit_y1.setMinimumSize(QSize(0, 25))
        self.lineEdit_y1.setObjectName("lineEdit_y1")
        self.lineEdit_y1.setText('0.0')

        self.y1_line.addWidget(self.lineEdit_y1)

        self.point_1.addLayout(self.y1_line)
        self.point_1.setStretch(0, 1)
        self.point_1.setStretch(1, 4)
        self.point_1.setStretch(2, 4)

        self.layout_input_two_points.addLayout(self.point_1)

        self.line_between_points = QFrame(self.two_points)
        self.line_between_points.setFrameShape(QFrame.VLine)
        self.line_between_points.setFrameShadow(QFrame.Sunken)
        self.line_between_points.setObjectName("line_between_points")

        self.layout_input_two_points.addWidget(self.line_between_points)

        self.point_2 = QVBoxLayout()
        self.point_2.setObjectName("point_2")

        self.label_point_2 = QLabel(self.two_points)
        self.label_point_2.setObjectName("label_point_2")
        self.label_point_2.setText(self._translate("GeometryWindow",
                                                   "<html><head/><body><p><span style=\" font-size:10pt;\">Введите координаты второй точки</span></p></body></html>"))

        self.point_2.addWidget(self.label_point_2)

        self.x2_line = QHBoxLayout()
        self.x2_line.setObjectName("x2_line")
        self.label_x2 = QLabel(self.two_points)
        self.label_x2.setObjectName("label_x2")
        self.label_x2.setText(self._translate("GeometryWindow",
                                              "<html><head/><body><p><span style=\" font-size:10pt;\">x2</span></p></body></html>"))
        self.x2_line.addWidget(self.label_x2)

        self.lineEdit_x2 = QLineEdit(self.two_points)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_x2.sizePolicy().hasHeightForWidth())
        self.lineEdit_x2.setSizePolicy(sizePolicy)
        self.lineEdit_x2.setMinimumSize(QSize(0, 25))
        self.lineEdit_x2.setObjectName("lineEdit_x2")

        self.x2_line.addWidget(self.lineEdit_x2)
        self.point_2.addLayout(self.x2_line)

        self.y2_line = QHBoxLayout()
        self.y2_line.setObjectName("y2_line")

        self.label_y2 = QLabel(self.two_points)
        self.label_y2.setObjectName("label_y2")
        self.label_y2.setText(self._translate("GeometryWindow",
                                              "<html><head/><body><p><span style=\" font-size:10pt;\">y2</span></p></body></html>"))

        self.y2_line.addWidget(self.label_y2)

        self.lineEdit_y2 = QLineEdit(self.two_points)
        self.lineEdit_y2.setMinimumSize(QSize(0, 25))
        self.lineEdit_y2.setObjectName("lineEdit_y2")

        self.y2_line.addWidget(self.lineEdit_y2)

        self.point_2.addLayout(self.y2_line)
        self.point_2.setStretch(0, 1)
        self.point_2.setStretch(1, 4)
        self.point_2.setStretch(2, 4)

        self.layout_input_two_points.addLayout(self.point_2)

        self.two_points_layout.addLayout(self.layout_input_two_points)

        self.layout_build_line = QHBoxLayout()
        self.layout_build_line.setObjectName("layout_build_line")

        self.label_units = QLabel(self.two_points)
        self.label_units.setObjectName("label_units")
        self.label_units.setText(self._translate("GeometryWindow",
                                                 "<html><head/><body><p><span style=\" font-size:10pt;\">Единицы измерения</span></p></body></html>"))

        self.layout_build_line.addWidget(self.label_units)

        self.combobox_units = QComboBox(self.two_points)
        self.combobox_units.setObjectName('combobox_units')
        self.combobox_units.addItems(['Милиметры', 'Сантиметры', 'Метры'])

        self.layout_build_line.addWidget(self.combobox_units)

        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layout_build_line.addItem(spacerItem)

        self.button_line_2_p = QPushButton(self.two_points)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_line_2_p.sizePolicy().hasHeightForWidth())
        self.button_line_2_p.setSizePolicy(sizePolicy)
        self.button_line_2_p.setObjectName("button_line_2_p")
        self.button_line_2_p.setText(self._translate("GeometryWindow", "Построить линию"))
        self.button_line_2_p.clicked.connect(self.add_line)

        self.layout_build_line.addWidget(self.button_line_2_p)

        # self.layout_build_line.setStretch(0, 0)
        # self.layout_build_line.setStretch(1, 0)
        self.layout_build_line.setStretch(2, 3)
        self.layout_build_line.setStretch(3, 1)

        self.two_points_layout.addLayout(self.layout_build_line)

        self.label_output = QLabel(self.two_points)
        self.label_output.setText("")
        self.label_output.setObjectName("label_output")
        self.two_points_layout.addWidget(self.label_output)

        spacerItem1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.two_points_layout.addItem(spacerItem1)

        self.layout_finally_geometry = QHBoxLayout()
        self.layout_finally_geometry.setObjectName("layout_finally_geometry")
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layout_finally_geometry.addItem(spacerItem2)

        self.button_finally_geometry = QPushButton(self.two_points)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_finally_geometry.sizePolicy().hasHeightForWidth())
        self.button_finally_geometry.setSizePolicy(sizePolicy)
        self.button_finally_geometry.setObjectName("button_finally_geometry")
        self.button_finally_geometry.setText(self._translate("GeometryWindow", "Завершить построение"))
        self.button_finally_geometry.clicked.connect(self.finally_geometry)

        self.layout_finally_geometry.addWidget(self.button_finally_geometry)
        spacerItem3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layout_finally_geometry.addItem(spacerItem3)
        self.layout_finally_geometry.setStretch(0, 1)
        self.layout_finally_geometry.setStretch(1, 1)
        self.layout_finally_geometry.setStretch(2, 1)

        self.two_points_layout.addLayout(self.layout_finally_geometry)

        self.two_points_layout.setStretch(0, 6)
        self.two_points_layout.setStretch(1, 2)
        self.two_points_layout.setStretch(2, 2)
        self.two_points_layout.setStretch(3, 10)
        self.two_points_layout.setStretch(4, 3)

    def add_line(self):
        s = ''
        x1 = self.lineEdit_x1.text().replace(',', '.')
        x2 = self.lineEdit_x2.text().replace(',', '.')
        y1 = self.lineEdit_y1.text().replace(',', '.')
        y2 = self.lineEdit_y2.text().replace(',', '.')
        try:
            x1 = float(x1)
        except ValueError:
            s += 'Координата x1 введена неправильно!\n'

        try:
            x2 = float(x2)
        except ValueError:
            s += 'Координата x2 введена неправильно!\n'

        try:
            y1 = float(y1)
        except ValueError:
            s += 'Координата y1 введена неправильно!\n'

        try:
            y2 = float(y2)
        except ValueError:
            s += 'Координата y2 введена неправильно!'

        if s:
            self.label_output.setText(s)
        else:
            self.label_output.setText('Линия построена!')
            self.lineEdit_x1.setText(str(x2))
            self.lineEdit_y1.setText(str(y2))
            self.lineEdit_x2.setText('')
            self.lineEdit_y2.setText('')

            self.count_lines += 1
            self.graphics.add_line_to_scene(x1, y1, x2, y2, self.count_lines)

    def finally_geometry(self):
        self.main_window.action_calculation.setEnabled(True)
