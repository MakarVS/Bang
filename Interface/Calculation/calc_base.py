import pandas as pd

from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QLayout, QHBoxLayout, QLabel, \
    QLineEdit, QFrame, QSizePolicy, QSpacerItem, QPushButton, \
    QGridLayout, QComboBox, QTreeWidgetItem, QMainWindow, QApplication
from PyQt5.QtCore import Qt, QSize, QCoreApplication, pyqtSlot, QPoint
from PyQt5.QtGui import QPolygonF, QPainter, QBrush, QPen

from Interface.Geometry.point import Point
from Calculations import calculations_one_velocity, calculations_pneum, calculations_thermo


class CalculationWindow(QWidget):

    def __init__(self, main_window, horizontal, tree, graphics):
        self._translate = QCoreApplication.translate
        super(CalculationWindow, self).__init__()

        self.gas_base = pd.read_pickle('bases/gas_base.pkl')
        self.powder_base = pd.read_pickle('bases/powder_base.pkl')
        self.materials_base = pd.read_pickle('bases/materials_base.pkl')

        self.count_lines = 0

        self.main_window = main_window

        self.get_tab_widget(horizontal)
        self.tree = tree

        self.graphics = graphics

        self.border_cam = None
        self.points_wall_list = []
        self.points_geom_barell_list = []

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
        self.get_base_params()
        self.get_params_powder()
        self.get_params_gas()
        self.get_params_materials()
        self.tabWidget.setTabEnabled(self.tabWidget.indexOf(self.params_gas), False)

    def get_base_params(self):
        self.base_params = QWidget()
        self.base_params.setObjectName("base_params")
        self.verticalLayout = QVBoxLayout(self.base_params)
        self.verticalLayout.setObjectName("verticalLayout")

        # gridLayout_fields
        self.gridLayout_fields = QGridLayout()
        self.gridLayout_fields.setContentsMargins(-1, 5, -1, -1)
        self.gridLayout_fields.setHorizontalSpacing(15)
        self.gridLayout_fields.setVerticalSpacing(25)
        self.gridLayout_fields.setObjectName("gridLayout_fields")

        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_fields.addItem(spacerItem, 0, 8, 1, 1)

        self.line_3 = QFrame(self.base_params)
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout_fields.addWidget(self.line_3, 0, 4, 6, 1)

        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_fields.addItem(spacerItem1, 0, 5, 1, 1)

        self.label_q = QLabel(self.base_params)
        self.label_q.setObjectName("label_q")
        self.label_q.setText(self._translate("MainWindow", "Масса снаряда"))
        self.gridLayout_fields.addWidget(self.label_q, 0, 0, 1, 1)

        self.lineEdit_q = QLineEdit(self.base_params)
        self.lineEdit_q.setObjectName("lineEdit_q")
        self.gridLayout_fields.addWidget(self.lineEdit_q, 0, 1, 1, 1)

        self.comboBox_q = QComboBox(self.base_params)
        self.comboBox_q.setObjectName("comboBox_q")
        self.comboBox_q.addItems(['Граммы', 'Килограммы'])
        self.gridLayout_fields.addWidget(self.comboBox_q, 0, 2, 1, 1)

        self.label_T_env = QLabel(self.base_params)
        self.label_T_env.setObjectName("label_T_env")
        self.label_T_env.setText(self._translate("MainWindow", "Температура окражающей среды"))
        self.gridLayout_fields.addWidget(self.label_T_env, 1, 0, 1, 1)

        self.lineEdit_T_env = QLineEdit(self.base_params)
        self.lineEdit_T_env.setObjectName("lineEdit_T_env")
        self.gridLayout_fields.addWidget(self.lineEdit_T_env, 1, 1, 1, 1)

        self.comboBox_T_env = QComboBox(self.base_params)
        self.comboBox_T_env.setObjectName("comboBox_T_env")
        self.comboBox_T_env.addItems(['К', '⁰С'])
        self.gridLayout_fields.addWidget(self.comboBox_T_env, 1, 2, 1, 1)

        self.label_type = QLabel(self.base_params)
        self.label_type.setObjectName("label_type")
        self.label_type.setText(self._translate("MainWindow", "Тип рабочего тела"))
        self.gridLayout_fields.addWidget(self.label_type, 2, 0, 1, 1)

        self.comboBox_type = QComboBox(self.base_params)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_type.sizePolicy().hasHeightForWidth())
        self.comboBox_type.setSizePolicy(sizePolicy)
        self.comboBox_type.setObjectName("comboBox_type")
        self.comboBox_type.addItems(['Порох', 'Газ'])
        self.comboBox_type.currentIndexChanged.connect(self.change_work_body)
        self.gridLayout_fields.addWidget(self.comboBox_type, 2, 1, 1, 1)

        self.label_border_cam = QLabel(self.base_params)
        self.label_border_cam.setObjectName("label_border_cam")
        self.label_border_cam.setText(self._translate("MainWindow","Выберите правую границу\n"
                                                                   "камеры сгорания"))
        self.gridLayout_fields.addWidget(self.label_border_cam, 3, 0, 1, 1)

        self.lineEdit_border_cam = QLineEdit(self.base_params)
        self.lineEdit_border_cam.setObjectName("lineEdit_border_cam")
        self.gridLayout_fields.addWidget(self.lineEdit_border_cam, 3, 1, 1, 1)

        self.pushButton_border_cam = QPushButton(self.base_params)
        self.pushButton_border_cam.setObjectName("pushButton_border_cam")
        self.pushButton_border_cam.clicked.connect(self.choose_border_cam_true)
        self.pushButton_border_cam.setText(self._translate("MainWindow", "Выбрать"))
        self.gridLayout_fields.addWidget(self.pushButton_border_cam, 3, 2, 1, 1)

        self.label_points_geom_barell = QLabel(self.base_params)
        self.label_points_geom_barell.setObjectName("label_points_geom_barell")
        self.label_points_geom_barell.setText(self._translate("MainWindow", "Выберите точки, через\n"
                                                                            "которые проходит внутренняя\n"
                                                                            "стенка канала ствола"))
        self.gridLayout_fields.addWidget(self.label_points_geom_barell, 4, 0, 1, 1)

        self.lineEdit_points_geom_barell = QLineEdit(self.base_params)
        self.lineEdit_points_geom_barell.setObjectName("lineEdit_points_geom_barell")
        self.gridLayout_fields.addWidget(self.lineEdit_points_geom_barell, 4, 1, 1, 1)

        self.pushButton_points_geom_barell = QPushButton(self.base_params)
        self.pushButton_points_geom_barell.setObjectName("pushButton_points_geom_barell")
        self.pushButton_points_geom_barell.setText(self._translate("MainWindow", "Выбрать"))
        self.pushButton_points_geom_barell.clicked.connect(self.choose_points_geom_barell_true)
        self.gridLayout_fields.addWidget(self.pushButton_points_geom_barell, 4, 2, 1, 1)

        self.pushButton_points_geom_barell_finaly = QPushButton(self.base_params)
        self.pushButton_points_geom_barell_finaly.setObjectName("pushButton_points_geom_barell_finaly")
        self.pushButton_points_geom_barell_finaly.setText(self._translate("MainWindow", "Завершить"))
        self.pushButton_points_geom_barell_finaly.clicked.connect(self.choose_points_geom_barell_false)
        self.gridLayout_fields.addWidget(self.pushButton_points_geom_barell_finaly, 4, 3, 1, 1)

        self.label_points_wall = QLabel(self.base_params)
        self.label_points_wall.setObjectName("label_points_wall")
        self.label_points_wall.setText(self._translate("MainWindow", "Выберите точки, которые \n"
                                                                     "ограничивают периметр \n"
                                                                     "стенки ствола"))
        self.gridLayout_fields.addWidget(self.label_points_wall, 5, 0, 1, 1)

        self.lineEdit_points_wall = QLineEdit(self.base_params)
        self.lineEdit_points_wall.setObjectName("lineEdit_points_wall")
        self.gridLayout_fields.addWidget(self.lineEdit_points_wall, 5, 1, 1, 1)

        self.pushButton_points_wall = QPushButton(self.base_params)
        self.pushButton_points_wall.setObjectName("pushButton_points_wall")
        self.pushButton_points_wall.setText(self._translate("MainWindow", "Выбрать"))
        self.pushButton_points_wall.clicked.connect(self.choose_points_wall_true)
        self.gridLayout_fields.addWidget(self.pushButton_points_wall, 5, 2, 1, 1)

        self.pushButton_points_wall_finaly = QPushButton(self.base_params)
        self.pushButton_points_wall_finaly.setObjectName("pushButton_points_wall_finaly")
        self.pushButton_points_wall_finaly.setText(self._translate("MainWindow", "Завершить"))
        self.pushButton_points_wall_finaly.clicked.connect(self.choose_points_wall_false)
        self.gridLayout_fields.addWidget(self.pushButton_points_wall_finaly, 5, 3, 1, 1)

        # self.label_charact_calc = QLabel(self.base_params)
        # self.label_charact_calc.setObjectName("label_charact_calc")
        # self.label_charact_calc.setText(self._translate("MainWindow", "Характеристики расчета"))
        # self.gridLayout_fields.addWidget(self.label_charact_calc, 0, 6, 1, 2)
        #
        # self.line_charact_calc = QFrame(self.base_params)
        # self.line_charact_calc.setFrameShape(QFrame.HLine)
        # self.line_charact_calc.setFrameShadow(QFrame.Sunken)
        # self.line_charact_calc.setObjectName("line_charact_calc")
        # self.gridLayout_fields.addWidget(self.line_charact_calc, 1, 6, 1, 2)

        self.label_n_cells = QLabel(self.base_params)
        self.label_n_cells.setObjectName("label_n_cells")
        self.label_n_cells.setText(self._translate("MainWindow", "Количество узлов разностной сетки\n"
                                                                 "по осевой координате"))
        self.gridLayout_fields.addWidget(self.label_n_cells, 0, 6, 1, 1)

        self.lineEdit_n_cells = QLineEdit(self.base_params)
        self.lineEdit_n_cells.setObjectName("lineEdit_n_cells")
        self.lineEdit_n_cells.setText('100')
        self.gridLayout_fields.addWidget(self.lineEdit_n_cells, 0, 7, 1, 1)

        self.label_n_cells_r = QLabel(self.base_params)
        self.label_n_cells_r.setObjectName("label_n_cells_r")
        self.label_n_cells_r.setText(self._translate("MainWindow", "Количество узлов разностной сетки\n"
                                                                   "по радиальной координате"))
        self.gridLayout_fields.addWidget(self.label_n_cells_r, 1, 6, 1, 1)

        self.lineEdit_n_cells_r = QLineEdit(self.base_params)
        self.lineEdit_n_cells_r.setObjectName("lineEdit_n_cells_r")
        self.lineEdit_n_cells_r.setText('100')
        self.gridLayout_fields.addWidget(self.lineEdit_n_cells_r, 1, 7, 1, 1)

        self.label_Ku = QLabel(self.base_params)
        self.label_Ku.setObjectName("label_Ku")
        self.label_Ku.setText(self._translate("MainWindow", "Число Куранта"))
        self.gridLayout_fields.addWidget(self.label_Ku, 2, 6, 1, 1)

        self.lineEdit_Ku = QLineEdit(self.base_params)
        self.lineEdit_Ku.setObjectName("lineEdit_Ku")
        self.lineEdit_Ku.setText('0.15')
        self.gridLayout_fields.addWidget(self.lineEdit_Ku, 2, 7, 1, 1)

        self.label_n_shoots = QLabel(self.base_params)
        self.label_n_shoots.setObjectName("label_n_shoots")
        self.label_n_shoots.setText(self._translate("MainWindow", "Количество выстрелов"))
        self.gridLayout_fields.addWidget(self.label_n_shoots, 3, 6, 1, 1)

        self.lineEdit_n_shoots = QLineEdit(self.base_params)
        self.lineEdit_n_shoots.setObjectName("lineEdit_n_shoots")
        self.lineEdit_n_shoots.setText('1')
        self.gridLayout_fields.addWidget(self.lineEdit_n_shoots, 3, 7, 1, 1)

        self.label_t_end = QLabel(self.base_params)
        self.label_t_end.setObjectName("label_t_end")
        self.label_t_end.setText(self._translate("MainWindow", "Время расчета теплопередачи, c"))
        self.gridLayout_fields.addWidget(self.label_t_end, 4, 6, 1, 1)

        self.lineEdit_t_end = QLineEdit(self.base_params)
        self.lineEdit_t_end.setObjectName("lineEdit_t_end")
        self.lineEdit_t_end.setText('1')
        self.gridLayout_fields.addWidget(self.lineEdit_t_end, 4, 7, 1, 1)

        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_fields.addItem(spacerItem2, 0, 3, 1, 1)

        self.gridLayout_fields.setColumnStretch(0, 2)
        self.gridLayout_fields.setColumnStretch(1, 3)
        self.gridLayout_fields.setColumnStretch(2, 1)
        self.gridLayout_fields.setColumnStretch(3, 1)
        self.gridLayout_fields.setColumnStretch(4, 1)
        self.gridLayout_fields.setColumnStretch(5, 1)
        self.gridLayout_fields.setColumnStretch(6, 3)
        self.gridLayout_fields.setColumnStretch(7, 3)
        self.gridLayout_fields.setColumnStretch(8, 2)
        self.gridLayout_fields.setRowStretch(0, 2)
        self.verticalLayout.addLayout(self.gridLayout_fields)

        spacerItem3 = QSpacerItem(20, 209, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)

        self.horizontalLayout_button = QHBoxLayout()
        self.horizontalLayout_button.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout_button.setObjectName("horizontalLayout_button")

        spacerItem4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_button.addItem(spacerItem4)

        self.pushButton_calc = QPushButton(self.base_params)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_calc.sizePolicy().hasHeightForWidth())
        self.pushButton_calc.setSizePolicy(sizePolicy)
        self.pushButton_calc.setObjectName("pushButton_calc")
        self.pushButton_calc.setText(self._translate("MainWindow", "Запустить расчёт"))
        self.pushButton_calc.clicked.connect(self.run_calculations_run)
        self.horizontalLayout_button.addWidget(self.pushButton_calc)

        spacerItem5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_button.addItem(spacerItem5)
        self.horizontalLayout_button.setStretch(0, 1)
        self.horizontalLayout_button.setStretch(1, 1)
        self.horizontalLayout_button.setStretch(2, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_button)
        self.verticalLayout.setStretch(0, 3)
        self.verticalLayout.setStretch(1, 9)
        self.verticalLayout.setStretch(2, 13)

        self.tabWidget.addTab(self.base_params, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.base_params),
                                  self._translate("MainWindow", "Основные параметры"))

    def get_params_powder(self):
        self.params_powder = QWidget()
        self.params_powder.setObjectName("params_powder")

        self.verticalLayout_4 = QVBoxLayout(self.params_powder)
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        self.horizontalLayout_work_body = QHBoxLayout()
        self.horizontalLayout_work_body.setSpacing(6)
        self.horizontalLayout_work_body.setObjectName("horizontalLayout_work_body")

        self.gridLayout_base_powder = QGridLayout()
        self.gridLayout_base_powder.setVerticalSpacing(15)
        self.gridLayout_base_powder.setObjectName("gridLayout_base_powder")

        self.label_mark = QLabel(self.params_powder)
        self.label_mark.setObjectName("label_mark")
        self.label_mark.setText(self._translate("MainWindow", "Марка пороха"))
        self.gridLayout_base_powder.addWidget(self.label_mark, 0, 0, 1, 1)

        self.comboBox_mark = QComboBox(self.params_powder)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_mark.sizePolicy().hasHeightForWidth())
        self.comboBox_mark.setSizePolicy(sizePolicy)
        self.comboBox_mark.setObjectName("comboBox_mark")
        powder_list = ['Другой порох']
        powder_list.extend(list(self.powder_base['name'].unique()))
        self.comboBox_mark.addItems(powder_list)
        self.comboBox_mark.currentIndexChanged.connect(self.change_type_powder)
        self.gridLayout_base_powder.addWidget(self.comboBox_mark, 0, 1, 1, 1)

        spacerItem6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_base_powder.addItem(spacerItem6, 0, 2, 1, 1)

        self.label_omega = QLabel(self.params_powder)
        self.label_omega.setObjectName("label_omega")
        self.label_omega.setText(self._translate("MainWindow", "Масса навески пороха"))
        self.gridLayout_base_powder.addWidget(self.label_omega, 1, 0, 1, 1)

        self.lineEdit_omega = QLineEdit(self.params_powder)
        self.lineEdit_omega.setObjectName("lineEdit_omega")
        self.gridLayout_base_powder.addWidget(self.lineEdit_omega, 1, 1, 1, 1)

        self.comboBox_omega = QComboBox(self.params_powder)
        self.comboBox_omega.setObjectName("comboBox_omega")
        self.comboBox_omega.addItems(['Граммы', 'Килограммы'])
        self.gridLayout_base_powder.addWidget(self.comboBox_omega, 1, 2, 1, 1)

        self.label_pf = QLabel(self.params_powder)
        self.label_pf.setObjectName("label_pf")
        self.label_pf.setText(self._translate("MainWindow", "Давление форсирования"))
        self.gridLayout_base_powder.addWidget(self.label_pf, 2, 0, 1, 1)

        self.lineEdit_pf = QLineEdit(self.params_powder)
        self.lineEdit_pf.setObjectName("lineEdit_pf")
        self.gridLayout_base_powder.addWidget(self.lineEdit_pf, 2, 1, 1, 1)

        self.comboBox_pf = QComboBox(self.params_powder)
        self.comboBox_pf.setObjectName("comboBox_pf")
        self.comboBox_pf.addItems(['МПа', 'Па'])
        self.gridLayout_base_powder.addWidget(self.comboBox_pf, 2, 2, 1, 1)

        self.label = QLabel(self.params_powder)
        self.label.setText("")
        self.label.setObjectName("label")

        self.gridLayout_base_powder.addWidget(self.label, 3, 0, 1, 1)
        self.gridLayout_base_powder.setColumnStretch(0, 4)
        self.gridLayout_base_powder.setColumnStretch(1, 4)
        self.gridLayout_base_powder.setColumnStretch(2, 1)
        self.gridLayout_base_powder.setRowStretch(0, 2)
        self.gridLayout_base_powder.setRowStretch(1, 1)
        self.gridLayout_base_powder.setRowStretch(2, 1)
        self.gridLayout_base_powder.setRowStretch(3, 16)
        self.horizontalLayout_work_body.addLayout(self.gridLayout_base_powder)

        spacerItem7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_work_body.addItem(spacerItem7)

        self.line_2 = QFrame(self.params_powder)
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_work_body.addWidget(self.line_2)

        spacerItem8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_work_body.addItem(spacerItem8)

        self.verticalLayout_charact_powder = QVBoxLayout()
        self.verticalLayout_charact_powder.setSpacing(15)
        self.verticalLayout_charact_powder.setObjectName("verticalLayout_charact_powder")

        self.label_params_powder = QLabel(self.params_powder)
        self.label_params_powder.setObjectName("label_params_powder")
        self.label_params_powder.setText(self._translate("MainWindow", "Характеристики пороха"))
        self.verticalLayout_charact_powder.addWidget(self.label_params_powder)

        self.line_params_powder = QFrame(self.params_powder)
        self.line_params_powder.setFrameShape(QFrame.HLine)
        self.line_params_powder.setFrameShadow(QFrame.Sunken)
        self.line_params_powder.setObjectName("line_params_powder")
        self.verticalLayout_charact_powder.addWidget(self.line_params_powder)

        self.gridLayout_charact_wo_coef = QGridLayout()
        self.gridLayout_charact_wo_coef.setVerticalSpacing(15)
        self.gridLayout_charact_wo_coef.setObjectName("gridLayout_charact_wo_coef")

        self.label_Ik = QLabel(self.params_powder)
        self.label_Ik.setObjectName("label_Ik")
        self.label_Ik.setText(self._translate("MainWindow", "Импульс конца горения пороха, МПа ∙ с"))
        self.gridLayout_charact_wo_coef.addWidget(self.label_Ik, 0, 0, 1, 1)

        self.lineEdit_Ik = QLineEdit(self.params_powder)
        self.lineEdit_Ik.setObjectName("lineEdit_Ik")
        self.gridLayout_charact_wo_coef.addWidget(self.lineEdit_Ik, 0, 1, 1, 1)

        self.label_f = QLabel(self.params_powder)
        self.label_f.setObjectName("label_f")
        self.label_f.setText(self._translate("MainWindow", "Сила пороха, МДж/кг"))
        self.gridLayout_charact_wo_coef.addWidget(self.label_f, 1, 0, 1, 1)

        self.lineEdit_f = QLineEdit(self.params_powder)
        self.lineEdit_f.setObjectName("lineEdit_f")
        self.gridLayout_charact_wo_coef.addWidget(self.lineEdit_f, 1, 1, 1, 1)

        self.label_rho = QLabel(self.params_powder)
        self.label_rho.setText(self._translate("MainWindow",
                                               "<html><head/><body><p>Плотность пороха, кг/дм<span style=\" "
                                               "vertical-align:super;\">3</span></p></body></html>"))
        self.label_rho.setObjectName("label_rho")
        self.gridLayout_charact_wo_coef.addWidget(self.label_rho, 2, 0, 1, 1)

        self.lineEdit_rho = QLineEdit(self.params_powder)
        self.lineEdit_rho.setObjectName("lineEdit_rho")
        self.gridLayout_charact_wo_coef.addWidget(self.lineEdit_rho, 2, 1, 1, 1)

        self.label_gamma = QLabel(self.params_powder)
        self.label_gamma.setObjectName("label_gamma")
        self.label_gamma.setText(self._translate("MainWindow", "Показатель адиабаты пороховых газов"))
        self.gridLayout_charact_wo_coef.addWidget(self.label_gamma, 3, 0, 1, 1)

        self.lineEdit_gamma = QLineEdit(self.params_powder)
        self.lineEdit_gamma.setObjectName("lineEdit_gamma")
        self.lineEdit_gamma.setText('')
        self.gridLayout_charact_wo_coef.addWidget(self.lineEdit_gamma, 3, 1, 1, 1)

        self.label_covolum = QLabel(self.params_powder)
        self.label_covolum.setObjectName("label_covolum")
        self.label_covolum.setText(self._translate("MainWindow",
                                              "<html><head/><body><p>Коволюм единицы массы пороховых газов, дм"
                                              "<span style=\" vertical-align:super;\">3</span>/кг</p></body></html>"))
        self.gridLayout_charact_wo_coef.addWidget(self.label_covolum, 4, 0, 1, 1)

        self.lineEdit_covolum = QLineEdit(self.params_powder)
        self.lineEdit_covolum.setObjectName("lineEdit_covolum")
        self.gridLayout_charact_wo_coef.addWidget(self.lineEdit_covolum, 4, 1, 1, 1)

        self.label_zk = QLabel(self.params_powder)
        self.label_zk.setObjectName("label_zk")
        self.label_zk.setText(self._translate("MainWindow", "Относительная толщина конца горения пороха"))
        self.gridLayout_charact_wo_coef.addWidget(self.label_zk, 5, 0, 1, 1)

        self.lineEdit_zk = QLineEdit(self.params_powder)
        self.lineEdit_zk.setObjectName("lineEdit_zk")
        self.gridLayout_charact_wo_coef.addWidget(self.lineEdit_zk, 5, 1, 1, 1)

        self.label_T_1 = QLabel(self.params_powder)
        self.label_T_1.setObjectName("label_nu")
        self.label_T_1.setText(self._translate("MainWindow", "Температура поверхности горения\n"
                                                             "порохового зерна, К"))
        self.gridLayout_charact_wo_coef.addWidget(self.label_T_1, 6, 0, 1, 1)

        self.lineEdit_T_1 = QLineEdit(self.params_powder)
        self.lineEdit_T_1.setObjectName("lineEdit_nu")
        self.gridLayout_charact_wo_coef.addWidget(self.lineEdit_T_1, 6, 1, 1, 1)

        self.gridLayout_charact_wo_coef.setColumnStretch(0, 3)
        self.verticalLayout_charact_powder.addLayout(self.gridLayout_charact_wo_coef)

        self.verticalLayout_coef = QVBoxLayout()
        self.verticalLayout_coef.setSpacing(15)
        self.verticalLayout_coef.setObjectName("verticalLayout_coef")

        self.label_coeff_form_powder = QLabel(self.params_powder)
        self.label_coeff_form_powder.setObjectName("label_coeff_form_powder")
        self.label_coeff_form_powder.setText(self._translate("MainWindow",
                                                             "Коэффициенты характеризующие форму порохового заряда"))
        self.verticalLayout_coef.addWidget(self.label_coeff_form_powder)

        self.gridLayout_coef = QGridLayout()
        self.gridLayout_coef.setVerticalSpacing(15)
        self.gridLayout_coef.setObjectName("gridLayout_coef")

        self.label_lambda_1 = QLabel(self.params_powder)
        self.label_lambda_1.setObjectName("label_lambda_1")
        self.label_lambda_1.setText(self._translate("MainWindow",
                                               "<html><head/><body><p><span style=\" font-family:\'Calibri,"
                                               "sans-serif\'; font-size:11pt;\">λ</span></p></body></html>"))
        self.gridLayout_coef.addWidget(self.label_lambda_1, 0, 0, 1, 1)

        self.lineEdit_lambda1_1 = QLineEdit(self.params_powder)
        self.lineEdit_lambda1_1.setObjectName("lineEdit_lambda1_1")
        self.gridLayout_coef.addWidget(self.lineEdit_lambda1_1, 0, 1, 1, 1)

        self.label_kappa_1 = QLabel(self.params_powder)
        self.label_kappa_1.setObjectName("label_kappa_1")
        self.label_kappa_1.setText(self._translate("MainWindow",
                                              "<html><head/><body><p><span style=\" font-family:\'Calibri,sans-serif\';"
                                              " font-size:11pt;\">κ</span></p></body></html>"))
        self.gridLayout_coef.addWidget(self.label_kappa_1, 1, 0, 1, 1)

        self.lineEdit_kappa_1 = QLineEdit(self.params_powder)
        self.lineEdit_kappa_1.setObjectName("lineEdit_kappa_1")
        self.gridLayout_coef.addWidget(self.lineEdit_kappa_1, 1, 1, 1, 1)

        spacerItem9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_coef.addItem(spacerItem9, 0, 2, 1, 1)

        self.gridLayout_coef.setColumnStretch(0, 1)
        self.gridLayout_coef.setColumnStretch(1, 2)
        self.gridLayout_coef.setColumnStretch(2, 10)

        self.verticalLayout_coef.addLayout(self.gridLayout_coef)
        self.verticalLayout_charact_powder.addLayout(self.verticalLayout_coef)
        self.horizontalLayout_work_body.addLayout(self.verticalLayout_charact_powder)

        spacerItem10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_work_body.addItem(spacerItem10)
        self.horizontalLayout_work_body.setStretch(0, 7)
        self.horizontalLayout_work_body.setStretch(4, 7)
        self.horizontalLayout_work_body.setStretch(5, 1)
        self.verticalLayout_4.addLayout(self.horizontalLayout_work_body)

        spacerItem11 = QSpacerItem(20, 44, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem11)
        self.tabWidget.addTab(self.params_powder, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.params_powder),
                                  self._translate("MainWindow", "Параметры пороха"))

    def get_params_gas(self):
        self.params_gas = QWidget()
        self.params_gas.setObjectName("params_gas")

        self.verticalLayout_3 = QVBoxLayout(self.params_gas)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.horizontalLayout_params_gas = QHBoxLayout()
        self.horizontalLayout_params_gas.setObjectName("horizontalLayout_params_gas")

        self.gridLayout_base_gas = QGridLayout()
        self.gridLayout_base_gas.setContentsMargins(-1, 5, -1, -1)
        self.gridLayout_base_gas.setHorizontalSpacing(15)
        self.gridLayout_base_gas.setVerticalSpacing(33)
        self.gridLayout_base_gas.setObjectName("gridLayout_base_gas")

        self.label_kind_gas = QLabel(self.params_gas)
        self.label_kind_gas.setObjectName("label_kind_gas")
        self.label_kind_gas.setText(self._translate("MainWindow", "Газ"))
        self.gridLayout_base_gas.addWidget(self.label_kind_gas, 0, 0, 1, 1)

        self.comboBox_gas = QComboBox(self.params_gas)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_gas.sizePolicy().hasHeightForWidth())
        self.comboBox_gas.setSizePolicy(sizePolicy)
        self.comboBox_gas.setLayoutDirection(Qt.LeftToRight)
        self.comboBox_gas.setObjectName("comboBox_gas")
        self.comboBox_gas.addItems(['Воздух', 'Углекислый газ', 'Гелий'])
        self.comboBox_gas.currentIndexChanged.connect(self.change_type_gas)
        self.gridLayout_base_gas.addWidget(self.comboBox_gas, 0, 1, 1, 1)

        self.label_pressure_gas = QLabel(self.params_gas)
        self.label_pressure_gas.setObjectName("label_pressure_gas")
        self.label_pressure_gas.setText(self._translate("MainWindow", "Давление газа в камере"))
        self.gridLayout_base_gas.addWidget(self.label_pressure_gas, 1, 0, 1, 1)

        self.lineEdit_pressure_gas = QLineEdit(self.params_gas)
        self.lineEdit_pressure_gas.setObjectName("lineEdit_pressure_gas")
        self.gridLayout_base_gas.addWidget(self.lineEdit_pressure_gas, 1, 1, 1, 1)

        self.comboBox_pressure_gas = QComboBox(self.params_gas)
        self.comboBox_pressure_gas.setObjectName("comboBox_pressure_gas")
        self.comboBox_pressure_gas.addItems(['МПа', 'Па'])
        self.gridLayout_base_gas.addWidget(self.comboBox_pressure_gas, 1, 2, 1, 1)

        self.label_temp_gas = QLabel(self.params_gas)
        self.label_temp_gas.setObjectName("label_temp_gas")
        self.label_temp_gas.setText(self._translate("MainWindow", "Температура газа в камере"))
        self.gridLayout_base_gas.addWidget(self.label_temp_gas, 2, 0, 1, 1)

        self.lineEdit_temp_gas = QLineEdit(self.params_gas)
        self.lineEdit_temp_gas.setObjectName("lineEdit_temp_gas")
        self.gridLayout_base_gas.addWidget(self.lineEdit_temp_gas, 2, 1, 1, 1)

        self.comboBox_temp_gas = QComboBox(self.params_gas)
        self.comboBox_temp_gas.setObjectName("comboBox_temp_gas")
        self.comboBox_temp_gas.addItems(['К', '⁰С'])
        self.gridLayout_base_gas.addWidget(self.comboBox_temp_gas, 2, 2, 1, 1)

        self.horizontalLayout_params_gas.addLayout(self.gridLayout_base_gas)

        spacerItem12 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_params_gas.addItem(spacerItem12)

        self.verticalLayout_char_gas = QVBoxLayout()
        self.verticalLayout_char_gas.setObjectName("verticalLayout_char_gas")

        self.label_charact_gas = QLabel(self.params_gas)
        self.label_charact_gas.setObjectName("label_charact_gas")
        self.label_charact_gas.setText(self._translate("MainWindow", "Характеристики газа"))
        self.verticalLayout_char_gas.addWidget(self.label_charact_gas)

        self.line_gas = QFrame(self.params_gas)
        self.line_gas.setFrameShape(QFrame.HLine)
        self.line_gas.setFrameShadow(QFrame.Sunken)
        self.line_gas.setObjectName("line_gas")
        self.verticalLayout_char_gas.addWidget(self.line_gas)

        self.gridLayout_char_gas = QGridLayout()
        self.gridLayout_char_gas.setSpacing(15)
        self.gridLayout_char_gas.setObjectName("gridLayout_char_gas")

        self.label_R_gas = QLabel(self.params_gas)
        self.label_R_gas.setObjectName("label_R_gas")
        self.label_R_gas.setText(self._translate("MainWindow", "Газовая постоянная Дж/(кг ∙ К)"))
        self.gridLayout_char_gas.addWidget(self.label_R_gas, 0, 0, 1, 1)

        self.lineEdit_R_gas = QLineEdit(self.params_gas)
        self.lineEdit_R_gas.setObjectName("lineEdit_R_gas")
        self.lineEdit_R_gas.setText(str(self.gas_base[self.gas_base['name'] == 'Воздух']['R'].values[0]))
        self.gridLayout_char_gas.addWidget(self.lineEdit_R_gas, 0, 1, 1, 1)

        self.label_gamma_gas = QLabel(self.params_gas)
        self.label_gamma_gas.setObjectName("label_gamma_gas")
        self.label_gamma_gas.setText(self._translate("MainWindow", "Показатель адиабаты"))
        self.gridLayout_char_gas.addWidget(self.label_gamma_gas, 1, 0, 1, 1)

        self.lineEdit_gamma_gas = QLineEdit(self.params_gas)
        self.lineEdit_gamma_gas.setObjectName("lineEdit_gamma_gas")
        self.lineEdit_gamma_gas.setText(str(self.gas_base[self.gas_base['name'] == 'Воздух']['gamma'].values[0]))
        self.gridLayout_char_gas.addWidget(self.lineEdit_gamma_gas, 1, 1, 1, 1)

        self.label_covolum_gas = QLabel(self.params_gas)
        self.label_covolum_gas.setObjectName("label_covolum_gas")
        self.label_covolum_gas.setText(self._translate("MainWindow", "Коволюм"))
        self.gridLayout_char_gas.addWidget(self.label_covolum_gas, 2, 0, 1, 1)

        self.lineEdit_covolum_gas = QLineEdit(self.params_gas)
        self.lineEdit_covolum_gas.setObjectName("lineEdit_covolum_gas")
        self.lineEdit_covolum_gas.setText(str(self.gas_base[self.gas_base['name'] == 'Воздух']['covolum'].values[0]))
        self.gridLayout_char_gas.addWidget(self.lineEdit_covolum_gas, 2, 1, 1, 1)

        self.verticalLayout_char_gas.addLayout(self.gridLayout_char_gas)
        self.horizontalLayout_params_gas.addLayout(self.verticalLayout_char_gas)

        spacerItem13 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_params_gas.addItem(spacerItem13)
        self.horizontalLayout_params_gas.setStretch(0, 4)
        self.horizontalLayout_params_gas.setStretch(1, 1)
        self.horizontalLayout_params_gas.setStretch(2, 4)
        self.horizontalLayout_params_gas.setStretch(3, 1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_params_gas)

        spacerItem14 = QSpacerItem(20, 284, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem14)
        self.verticalLayout_3.setStretch(0, 2)
        self.verticalLayout_3.setStretch(1, 4)

        self.tabWidget.addTab(self.params_gas, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.params_gas),
                                  self._translate("MainWindow", "Параметры газа"))

    def get_params_materials(self):
        self.params_materials = QWidget()
        self.params_materials.setObjectName("params_materials")

        self.verticalLayout_6 = QVBoxLayout(self.params_materials)
        self.verticalLayout_6.setObjectName("verticalLayout_6")

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setSpacing(20)
        self.verticalLayout_5.setObjectName("verticalLayout_5")

        spacerItem15 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem15)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.label_materials = QLabel(self.params_materials)
        self.label_materials.setObjectName("label_materials")
        self.label_materials.setText(self._translate("MainWindow", "Материал ствола"))
        self.horizontalLayout_2.addWidget(self.label_materials)

        self.comboBox_materials = QComboBox(self.params_materials)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_materials.sizePolicy().hasHeightForWidth())
        self.comboBox_materials.setSizePolicy(sizePolicy)
        self.comboBox_materials.setObjectName("comboBox_materials")
        materials = ['Другой материал']
        materials.extend(list(self.materials_base['name'].unique()))
        self.comboBox_materials.addItems(materials)
        self.comboBox_materials.currentIndexChanged.connect(self.change_type_materials)
        self.horizontalLayout_2.addWidget(self.comboBox_materials)

        self.verticalLayout_5.addLayout(self.horizontalLayout_2)

        spacerItem16 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem16)

        self.verticalLayout_5.setStretch(0, 3)
        self.verticalLayout_5.setStretch(1, 2)
        self.verticalLayout_5.setStretch(2, 3)

        self.horizontalLayout_3.addLayout(self.verticalLayout_5)

        spacerItem17 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem17)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(15)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.label_char_materials = QLabel(self.params_materials)
        self.label_char_materials.setObjectName("label_char_materials")
        self.label_char_materials.setText(self._translate("MainWindow", "Характеристики матеирала"))
        self.verticalLayout_2.addWidget(self.label_char_materials)

        self.line_materials = QFrame(self.params_materials)
        self.line_materials.setFrameShape(QFrame.HLine)
        self.line_materials.setFrameShadow(QFrame.Sunken)
        self.line_materials.setObjectName("line_materials")
        self.verticalLayout_2.addWidget(self.line_materials)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setSpacing(20)
        self.gridLayout_3.setObjectName("gridLayout_3")

        self.label_rho_materials = QLabel(self.params_materials)
        self.label_rho_materials.setObjectName("label_rho_materials")
        self.label_rho_materials.setText(self._translate("MainWindow", "Плотность"))
        self.gridLayout_3.addWidget(self.label_rho_materials, 0, 0, 1, 1)

        self.lineEdit_rho_materials = QLineEdit(self.params_materials)
        self.lineEdit_rho_materials.setObjectName("lineEdit_rho_materials")
        self.gridLayout_3.addWidget(self.lineEdit_rho_materials, 0, 1, 1, 1)

        self.comboBox_rho_materials = QComboBox(self.params_materials)
        self.comboBox_rho_materials.setObjectName("comboBox_rho_materials")
        self.comboBox_rho_materials.addItems(['кг/м3', 'г/см3'])

        self.gridLayout_3.addWidget(self.comboBox_rho_materials, 0, 2, 1, 1)

        self.label_sigma_v = QLabel(self.params_materials)
        self.label_sigma_v.setObjectName("label_sigma_v")
        self.label_sigma_v.setText(self._translate("MainWindow", "Предел упругости, МПа"))
        self.gridLayout_3.addWidget(self.label_sigma_v, 1, 0, 1, 1)

        self.lineEdit_sigma_v = QLineEdit(self.params_materials)
        self.lineEdit_sigma_v.setObjectName("lineEdit_sigma_v")
        self.gridLayout_3.addWidget(self.lineEdit_sigma_v, 1, 1, 1, 1)

        self.label_lambda_materials = QLabel(self.params_materials)
        self.label_lambda_materials.setObjectName("label_lambda_materials")
        self.label_lambda_materials.setText(self._translate("MainWindow",
                                                              "<html><head/><body><p>Коэффициент теплопроводности, "
                                                              "Вт/(м ∙ ⁰С)</p></body></html>"))
        self.gridLayout_3.addWidget(self.label_lambda_materials, 2, 0, 1, 1)

        self.lineEdit_lambda_materials = QLineEdit(self.params_materials)
        self.lineEdit_lambda_materials.setObjectName("lineEdit_lambda_materials")
        self.gridLayout_3.addWidget(self.lineEdit_lambda_materials, 2, 1, 1, 1)

        self.label_cp_materials = QLabel(self.params_materials)
        self.label_cp_materials.setObjectName("label_cp_materials")
        self.label_cp_materials.setText(self._translate("MainWindow",
                                                        "<html><head/><body><p>Удельная теплоемкость при постоянном "
                                                        "давлении, Дж/(кг ∙ ⁰С)</p></body></html>"))
        self.gridLayout_3.addWidget(self.label_cp_materials, 3, 0, 1, 1)

        self.lineEdit_cp_materials = QLineEdit(self.params_materials)
        self.lineEdit_cp_materials.setObjectName("lineEdit_cp_materials")
        self.gridLayout_3.addWidget(self.lineEdit_cp_materials, 3, 1, 1, 1)

        self.verticalLayout_2.addLayout(self.gridLayout_3)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.setStretch(2, 5)

        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        spacerItem18 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem18)

        self.horizontalLayout_3.setStretch(0, 3)
        self.horizontalLayout_3.setStretch(1, 1)
        self.horizontalLayout_3.setStretch(2, 7)
        self.horizontalLayout_3.setStretch(3, 1)

        self.verticalLayout_6.addLayout(self.horizontalLayout_3)

        spacerItem19 = QSpacerItem(20, 228, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem19)

        self.verticalLayout_6.setStretch(0, 2)
        self.verticalLayout_6.setStretch(1, 3)

        self.tabWidget.addTab(self.params_materials, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.params_materials),
                                  self._translate("MainWindow", "Параметры материала ствола"))

    def change_work_body(self):
        text = self.comboBox_type.currentText()
        if text == 'Порох':
            self.tabWidget.setTabEnabled(self.tabWidget.indexOf(self.params_powder), True)
            self.tabWidget.setTabEnabled(self.tabWidget.indexOf(self.params_gas), False)
        elif text == 'Газ':
            self.tabWidget.setTabEnabled(self.tabWidget.indexOf(self.params_powder), False)
            self.tabWidget.setTabEnabled(self.tabWidget.indexOf(self.params_gas), True)

    def change_type_gas(self):
        text = self.comboBox_gas.currentText()
        self.lineEdit_R_gas.setText(str(self.gas_base[self.gas_base['name'] == text]['R'].values[0]))
        self.lineEdit_gamma_gas.setText(str(self.gas_base[self.gas_base['name'] == text]['gamma'].values[0]))
        self.lineEdit_covolum_gas.setText(str(self.gas_base[self.gas_base['name'] == text]['covolum'].values[0]))

    def change_type_powder(self):
        text = self.comboBox_mark.currentText()
        self.lineEdit_Ik.setText(str(round(self.powder_base[self.powder_base['name']
                                                            == text]['I_k'].values[0], 4)))
        self.lineEdit_f.setText(str(round(self.powder_base[self.powder_base['name']
                                                           == text]['f'].values[0], 4)))
        self.lineEdit_rho.setText(str(round(self.powder_base[self.powder_base['name']
                                                             == text]['ro'].values[0], 4)))
        self.lineEdit_gamma.setText(str(round(self.powder_base[self.powder_base['name']
                                                               == text]['etta'].values[0] + 1, 4)))
        self.lineEdit_T_1.setText(str(self.powder_base[self.powder_base['name'] == text]['T_1'].values[0]))
        self.lineEdit_covolum.setText(str(round(self.powder_base[self.powder_base['name']
                                                                 == text]['alpha_k'].values[0], 4)))
        self.lineEdit_zk.setText(str(round(self.powder_base[self.powder_base['name']
                                                            == text]['Z_k'].values[0], 4)))
        self.lineEdit_lambda1_1.setText(str(round(self.powder_base[self.powder_base['name']
                                                                   == text]['lambda_1'].values[0], 4)))
        self.lineEdit_kappa_1.setText(str(round(self.powder_base[self.powder_base['name']
                                                                 == text]['k_1'].values[0], 4)))

    def change_type_materials(self):
        text = self.comboBox_materials.currentText()
        self.lineEdit_rho_materials.setText(str(self.materials_base[self.materials_base['name']
                                                == text]['ro'].values[0]))
        self.lineEdit_cp_materials.setText(str(self.materials_base[self.materials_base['name']
                                               == text]['c_p'].values[0]))
        self.lineEdit_lambda_materials.setText(str(self.materials_base[self.materials_base['name']
                                                   == text]['lambda'].values[0]))
        self.lineEdit_sigma_v.setText(str(self.materials_base[self.materials_base['name']
                                          == text]['sigma'].values[0]))

    def choose_border_cam_true(self):
        for line_item in self.tree.model().rootItem.childItems[0].childItems:
            line_item.itemData[0][1].flag_mouse_event = True

    def choose_border_cam_false(self):
        for line_item in self.tree.model().rootItem.childItems[0].childItems:
            line_item.itemData[0][1].flag_mouse_event = False
        self.y_bord_cam = max(self.border_cam.line().y1(), self.border_cam.line().y2())
        self.x_bord_cam = self.border_cam.line().x2()
        point_1 = QPoint(self.graphics.init_delta_x, self.graphics.init_delta_y)
        point_2 = QPoint(self.graphics.init_delta_x, self.y_bord_cam)
        point_3 = QPoint(self.x_bord_cam, self.y_bord_cam)
        point_4 = QPoint(self.x_bord_cam, self.graphics.init_delta_y)

        camera = QPolygonF([point_1, point_2, point_3, point_4])
        self.graphics.graph_scene.addPolygon(camera, brush=QBrush(Qt.Dense7Pattern),
                                             pen=QPen(Qt.NoPen))

    def choose_points_wall_true(self):
        for line_item in self.tree.model().rootItem.childItems[0].childItems:
            for point in line_item.childItems:
                point.itemData[0][1].flag_points_wall = True

    def choose_points_wall_false(self):
        for line_item in self.tree.model().rootItem.childItems[0].childItems:
            for point in line_item.childItems:
                point.itemData[0][1].flag_points_wall = False

        point_list_for_polygon = []
        for point in self.points_wall_list:
            point_list_for_polygon.append(QPoint(point.x, point.y))

        wall = QPolygonF(point_list_for_polygon)
        self.graphics.graph_scene.addPolygon(wall, brush=QBrush(Qt.BDiagPattern),
                                             pen=QPen(Qt.NoPen))

    def choose_points_geom_barell_true(self):
        for line_item in self.tree.model().rootItem.childItems[0].childItems:
            for point in line_item.childItems:
                point.itemData[0][1].flag_points_geom_barell = True

    def choose_points_geom_barell_false(self):
        for line_item in self.tree.model().rootItem.childItems[0].childItems:
            for point in line_item.childItems:
                point.itemData[0][1].flag_points_geom_barell = False

    def run_calculations_run(self):
        q = self.lineEdit_q.text()
        T_env = self.lineEdit_T_env.text()
        bord = self.lineEdit_border_cam.text()
        wall_points = self.lineEdit_points_wall.text()
        geom_bar_points = self.lineEdit_points_geom_barell.text()
        points_wall = self.lineEdit_points_wall.text()
        n_cells = self.lineEdit_n_cells.text()
        n_cells_r = self.lineEdit_n_cells_r.text()
        Ku = self.lineEdit_Ku.text()
        n_shoots = self.lineEdit_n_shoots.text()
        t_end = self.lineEdit_t_end.text()

        rho_materials = self.lineEdit_rho_materials.text()
        sigma_v = self.lineEdit_sigma_v.text()
        lambda_materials = self.lineEdit_lambda_materials.text()
        cp_materials = self.lineEdit_cp_materials.text()

        if q and T_env and bord and wall_points and geom_bar_points and points_wall \
        and n_cells and n_cells_r and Ku and n_shoots and t_end\
        and rho_materials and sigma_v and lambda_materials and cp_materials:
            q = float(q.replace(',', '.'))
            q_dimension = self.comboBox_q.currentText()
            q = q if q_dimension == 'Килограммы' else (q / 1000)

            T_env = float(T_env.replace(',', '.'))
            T_env_dimension = self.comboBox_T_env.currentText()
            T_env = (T_env-273.15) if T_env_dimension == 'К' else T_env

            n_cells = int(n_cells)
            n_cells_r = int(n_cells_r)
            Ku = float(Ku.replace(',', '.'))
            n_shoots = int(n_shoots)
            t_end = float(t_end)

            rho_materials = float(rho_materials)
            sigma_v = float(sigma_v)
            lambda_materials = float(lambda_materials)
            cp_materials = float(cp_materials)

            units = self.tree.model().rootItem.childItems[0].itemData[0][1].combobox_units.currentText()
            if units == 'Милиметры':
                coef_units = 1000
            elif units == 'Сантиметры':
                coef_units = 100
            else:
                coef_units = 1

            x_bord_cam = (self.x_bord_cam - self.graphics.init_delta_x) / self.graphics.coef_scale / coef_units

            geom_barell = []
            for point in self.points_geom_barell_list:
                geom_barell.append(((point.x - self.graphics.init_delta_x) / self.graphics.coef_scale / coef_units,
                                    (point.y - self.graphics.init_delta_y) * 2 / self.graphics.coef_scale / coef_units))

            R_out = 0
            r_in = 100000000
            L = 0
            for point in self.points_wall_list:
                buf_L = (point.x - self.graphics.init_delta_x) / self.graphics.coef_scale / coef_units
                buf_r = (point.y - self.graphics.init_delta_y) / self.graphics.coef_scale / coef_units
                if buf_L > L:
                    L = buf_L
                if buf_r > R_out:
                    R_out = buf_r
                if buf_r < r_in:
                    r_in = buf_r

            text = self.comboBox_type.currentText()

            if text == 'Порох':
                I_k = self.lineEdit_Ik.text()
                Z_k = self.lineEdit_zk.text()
                alpha_k = self.lineEdit_covolum.text()
                etta = self.lineEdit_gamma.text()
                f = self.lineEdit_f.text()
                k_1 = self.lineEdit_kappa_1.text()
                lambda_1 = self.lineEdit_lambda1_1.text()
                ro = self.lineEdit_rho.text()
                T_1 = self.lineEdit_T_1.text()

                omega = self.lineEdit_omega.text()
                p_f = self.lineEdit_pf.text()

                if I_k and Z_k and alpha_k and etta and f and k_1 and lambda_1 and ro and T_1 and omega and p_f:
                    omega = float(omega.replace(',', '.'))
                    omega_dimension = self.comboBox_q.currentText()
                    omega = omega if omega_dimension == 'Килограммы' else (omega / 1000)

                    p_f = float(p_f.replace(',', '.'))
                    p_f_dimension = self.comboBox_pf.currentText()
                    p_f = p_f if p_f_dimension == 'Па' else (p_f * 1_000_000)

                    powder = dict(gamma=float(etta.replace(',', '.')) + 1,
                                  nu=1,
                                  param_powder={'I_k': float(I_k.replace(',', '.')),
                                                'Z_k': float(Z_k.replace(',', '.')),
                                                'alpha_k': float(alpha_k.replace(',', '.')),
                                                'etta': float(etta.replace(',', '.')) - 1,
                                                'T_1': float(T_1.replace(',', '.')),
                                                'f': float(f.replace(',', '.')),
                                                'k_1': float(k_1.replace(',', '.')),
                                                'k_2': None,
                                                'k_f': None,
                                                'k_l': None,
                                                'lambda_1': float(lambda_1.replace(',', '.')),
                                                'lambda_2': None,
                                                'name': self.comboBox_mark.currentText(),
                                                'ro': float(ro.replace(',', '.'))})
                    solver = calculations_one_velocity.solver(q=q,
                                                              p_f=p_f,
                                                              x_bord=x_bord_cam,
                                                              geom=geom_barell,
                                                              powder=powder,
                                                              omega=omega,
                                                              n_cells=n_cells,
                                                              Ku=Ku,
                                                              sigma_v=sigma_v,
                                                              R=R_out,
                                                              r=r_in)
                    self.main_window.change_statusbar('Идет рассчёт')
                    T_in = calculations_one_velocity.calc_run(solver)
                    self.main_window.change_statusbar('Рассчёт окончен')

                    solver_heat = calculations_thermo.solver_thermo(ro=rho_materials,
                                                                    cp=cp_materials,
                                                                    lambd=lambda_materials,
                                                                    n_x=n_cells,
                                                                    n_r=n_cells_r,
                                                                    L=L,
                                                                    R=R_out,
                                                                    r=r_in,
                                                                    t_end=t_end,
                                                                    T_env=T_env,
                                                                    T_in=T_in)

                    self.main_window.change_statusbar('Идет рассчёт')
                    calculations_thermo.calc_run(solver_heat)
                    self.main_window.change_statusbar('Рассчёт окончен')
                else:
                    self.main_window.change_statusbar('НЕ ВСЕ ПОЛЯ ЗАПОЛНЕНЫ!!!')
            elif text == 'Газ':
                p = self.lineEdit_pressure_gas.text()
                T = self.lineEdit_temp_gas.text()
                R = self.lineEdit_R_gas.text()
                gamma = self.lineEdit_gamma_gas.text()
                covolum = self.lineEdit_covolum_gas.text()

                if p and T and R and gamma and covolum:
                    p = float(p.replace(',', '.'))
                    p_dimension = self.comboBox_pressure_gas.currentText()
                    p = p if p_dimension == 'Па' else (p * 1_000_000)

                    T = float(T.replace(',', '.'))
                    T_dimension = self.comboBox_temp_gas.currentText()
                    T = T if T_dimension == 'К' else (T + 273.15)

                    gas = dict(R=float(R.replace(',', '.')), covolume=float(covolum.replace(',', '.')),
                               gamma=float(gamma.replace(',', '.')))

                    solver = calculations_pneum.solver(q=q,
                                                       x_bord=x_bord_cam,
                                                       geom=geom_barell,
                                                       gas=gas,
                                                       T=T,
                                                       p=p,
                                                       n_cells=n_cells,
                                                       Ku=Ku,
                                                       sigma_v=sigma_v,
                                                       R=R_out,
                                                       r=r_in)

                    # print(solver)
                    self.main_window.change_statusbar('Идет рассчёт')
                    T_in = calculations_pneum.calc_run(solver) - 273.15
                    self.main_window.change_statusbar('Рассчёт окончен')

                    solver_heat = calculations_thermo.solver_thermo(ro=rho_materials,
                                                                    cp=cp_materials,
                                                                    lambd=lambda_materials,
                                                                    n_x=n_cells,
                                                                    n_r=n_cells_r,
                                                                    L=L,
                                                                    R=R_out,
                                                                    r=r_in,
                                                                    t_end=t_end,
                                                                    T_env=T_env,
                                                                    T_in=T_in)

                    self.main_window.change_statusbar('Идет рассчёт')
                    calculations_thermo.calc_run(solver_heat)
                    self.main_window.change_statusbar('Рассчёт окончен')

                else:
                    self.main_window.change_statusbar('НЕ ВСЕ ПОЛЯ ЗАПОЛНЕНЫ!!!')
        else:
            self.main_window.change_statusbar('НЕ ВСЕ ПОЛЯ ЗАПОЛНЕНЫ!!!')
