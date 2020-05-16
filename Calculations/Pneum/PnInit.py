from Calculations.Pneum.PnLayer import PnLayer
from Calculations.Pneum.PnBorder import *


def func_in(x, grid):
    """
    Функция инициализации ячейки
    :param x: координата центра ячейки
    :return: значения параметров плотности, скорости и давления в ячейке
    """
    if x:
        ro = grid['init_const']['p'] / (grid['consts']['R'] * grid['init_const']['T'] +
                                        grid['init_const']['p'] * grid['consts']['covolume'])
        u = 0
        p = grid['init_const']['p']
        return ro, u, p


def pn_create_layer(solver):
    return PnLayer(solver, func_in, get_x_v_left, get_x_v_right, get_flux_left, get_flux_right)
