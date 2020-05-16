from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
import numpy as np

from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QComboBox
from PyQt5.QtCore import QCoreApplication

from Calculations.Invariants.Plot import set_axes
from Interface.Postprocessing.plot_canvas import PlotCanvas


class PostprocessingWindow(QWidget):

    def __init__(self, central_widget, calculations):
        self._translate = QCoreApplication.translate
        super(PostprocessingWindow, self).__init__()

        self.calculations = calculations
        self.get_tab_widget(central_widget)
        self.get_list_plot(central_widget)

    def get_tab_widget(self, central_widget):
        """
        Создание окна с вкладками для постпроцессинга
        :return:
        """
        self.tabWidget = QTabWidget(central_widget)
        self.tabWidget.setStyleSheet("backhround-color:rgb(156, 156, 156)")
        self.tabWidget.setTabPosition(QTabWidget.North)
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.tabWidget.setObjectName("tabWidget")

    def get_list_plot(self, central_widget):
        self.plot = QWidget(central_widget)
        self.plot.setObjectName("plot")

        self.plot_layout = QHBoxLayout(self.plot)
        self.plot_layout.setObjectName("plot_layout")

        self.left_plot_layout = QVBoxLayout(self.plot)
        self.left_plot_layout.setObjectName("left_plot_layout")

        self.comboBox_left_plot = QComboBox(self.plot)
        self.comboBox_left_plot.setObjectName("comboBox_left_plot")
        self.comboBox_left_plot.addItems(['График зависимости скорости от времени',
                                          'График зависимости скорости от координаты ствола',
                                          'График зависимости давления на дно снаряда от времени',
                                          'График зависимости давления на канала ствола от времени'])
        self.comboBox_left_plot.currentIndexChanged.connect(self.change_plot_left)
        self.left_plot_layout.addWidget(self.comboBox_left_plot)

        self.in_lay_left_plot = QVBoxLayout(self.plot)
        self.in_lay_left_plot.setObjectName("in_lay_left_plot")
        self.left_plot_layout.addLayout(self.in_lay_left_plot)
        # self.widget_left_plot = QWidget(self.plot)
        # self.widget_left_plot.setObjectName("widget_left_plot")
        # self.left_plot_layout.addWidget(self.widget_left_plot)

        self.plot_layout.addLayout(self.left_plot_layout)

        self.right_plot_layout = QVBoxLayout(self.plot)
        self.right_plot_layout.setObjectName("right_plot_layout")

        self.comboBox_right_plot = QComboBox(self.plot)
        self.comboBox_right_plot.setObjectName("comboBox_right_plot")
        self.comboBox_right_plot.addItems(['График зависимости давления на дно снаряда от времени',
                                           'График зависимости давления на канала ствола от времени',
                                           'График зависимости скорости от времени',
                                           'График зависимости скорости от координаты ствола'])
        self.comboBox_right_plot.currentIndexChanged.connect(self.change_plot_right)
        self.right_plot_layout.addWidget(self.comboBox_right_plot)

        # self.widget_right_plot = QWidget(self.plot)
        # self.widget_right_plot.setObjectName("widget_right_plot")
        # self.right_plot_layout.addWidget(self.widget_right_plot)
        self.in_lay_right_plot = QVBoxLayout(self.plot)
        self.in_lay_right_plot.setObjectName("in_lay_right_plot")
        self.right_plot_layout.addLayout(self.in_lay_right_plot)

        self.plot_layout.addLayout(self.right_plot_layout)

        self.plot_layout.setStretch(0, 1)
        self.plot_layout.setStretch(1, 1)

    def init_plot(self):
        fig, axes = set_axes(self.calculations.results[1]['time_arr'],
                             self.calculations.results[1]['V_arr'],
                             'График зависимости скорости снаряда от времени', 't, c', 'Vд, м/с')
        self.left_plot_canvas = PlotCanvas(fig)
        self.left_plot_canvas.fig.add_axes(axes)

        self.in_lay_left_plot.addWidget(self.left_plot_canvas)
        self.left_toolbar = NavigationToolbar2QT(self.left_plot_canvas, self.plot)
        self.in_lay_left_plot.addWidget(self.left_toolbar)

        fig, axes = set_axes(self.calculations.results[1]['time_arr'],
                             np.array(self.calculations.results[1]['p_arr_sn']) / 1_000_000,
                             'График зависимости давления на дно снаряда от времени', 't, c', 'p_sn, МПа')

        self.right_plot_canvas = PlotCanvas(fig)
        self.right_plot_canvas.fig.add_axes(axes)

        self.in_lay_right_plot.addWidget(self.right_plot_canvas)
        self.right_toolbar = NavigationToolbar2QT(self.right_plot_canvas, self.plot)
        self.in_lay_right_plot.addWidget(self.right_toolbar)

    def change_plot(self, text):
        if text == 'График зависимости скорости от времени':
            fig, axes = set_axes(self.calculations.results[1]['time_arr'],
                                 self.calculations.results[1]['V_arr'],
                                 'График зависимости скорости снаряда от времени', 't, c', 'Vд, м/с')
        elif text == 'График зависимости скорости от координаты ствола':
            fig, axes = set_axes(self.calculations.results[1]['x_arr'],
                                 self.calculations.results[1]['V_arr'],
                                 'График зависимости скорости от координаты ствола', 'x, м', 'Vд, м/с')
        elif text == 'График зависимости давления на дно снаряда от времени':
            fig, axes = set_axes(self.calculations.results[1]['time_arr'],
                                 np.array(self.calculations.results[1]['p_arr_sn']) / 1_000_000,
                                 'График зависимости давления на дно снаряда от времени', 't, c', 'p_sn, МПа')
        elif text == 'График зависимости давления на канала ствола от времени':
            fig, axes = set_axes(self.calculations.results[1]['time_arr'],
                                 np.array(self.calculations.results[1]['p_arr_dn']) / 1_000_000,
                                 'График зависимости давления на канала ствола от времени', 't, c', 'p_kn, МПа')

        plot_canvas = PlotCanvas(fig)
        plot_canvas.fig.add_axes(axes)

        return plot_canvas

    def change_plot_left(self):
        text = self.comboBox_left_plot.currentText()
        self.in_lay_left_plot.removeWidget(self.left_plot_canvas)
        self.in_lay_left_plot.removeWidget(self.left_toolbar)
        self.left_plot_canvas = self.change_plot(text)

        self.in_lay_left_plot.addWidget(self.left_plot_canvas)
        self.left_toolbar = NavigationToolbar2QT(self.left_plot_canvas, self.plot)
        self.in_lay_left_plot.addWidget(self.left_toolbar)

    def change_plot_right(self):
        text = self.comboBox_right_plot.currentText()
        self.in_lay_right_plot.removeWidget(self.right_plot_canvas)
        self.in_lay_right_plot.removeWidget(self.right_toolbar)
        self.right_plot_canvas = self.change_plot(text)

        self.in_lay_right_plot.addWidget(self.right_plot_canvas)
        self.right_toolbar = NavigationToolbar2QT(self.right_plot_canvas, self.plot)
        self.in_lay_right_plot.addWidget(self.right_toolbar)
