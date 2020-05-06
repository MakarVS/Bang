"""
Created on Wed Jan 17 10:53:30 2018

Создание геометрии ствола
"""

import numpy as np
from scipy import interpolate
from math import pi


class Tube(object):
    def __init__(self, xs, ds):
        self.d = interpolate.interp1d(xs, ds, bounds_error=False, fill_value=(ds[0], ds[-1]))
        dd = np.array(ds, dtype=np.float64)
        ss = dd ** 2 * pi * 0.25
        self.s = interpolate.interp1d(xs, ss, bounds_error=False, fill_value=(ss[0], ss[-1]))

    def get_stuff(self, xs):
        """
        return (ds)
        """
        x = np.array(xs, dtype=np.float64)

        x_right = np.roll(x, -1)

        dx = x_right - x

        s_l = self.s(x)
        s_r = self.s(x_right)

        ds = (s_r - s_l) / dx
        return ds[:-1]

    def get_W(self, xs):
        """
        Получение объема ячеек
        :param xs:
        :return:
        """
        x = np.array(xs, dtype=np.float64)

        x_right = np.roll(x, -1)

        dx = x_right - x

        s_l = self.s(x)
        s_r = self.s(x_right)

        W = (s_r + s_l + np.sqrt(s_l * s_r)) * dx / 3
        return W[:-1]

    def get_S(self, xs):
        """
        Получение площадей в узлах
        :param xs:
        :return:
        """
        x = np.array(xs, dtype=np.float64)
        s = self.s(x)
        return s
