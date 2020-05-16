from Calculations.OneVelocity.OvLayer import OvLayer
from Calculations.OneVelocity.OvBorder import *


def func_in(x, grid, W_km):
    """
    Функция инициализации ячейки
    :param x: координата центра ячейки
    :return: значения параметров плотности, скорости и давления в ячейке
    """
    if x:
        ro = grid['init_const']['omega'] / W_km
        u = 0
        p = 101325
        z = 0
        return ro, u, p, z


def ov_create_layer(solver):
    return OvLayer(solver, func_in, get_x_v_left, get_x_v_right, get_flux_left, get_flux_right)
