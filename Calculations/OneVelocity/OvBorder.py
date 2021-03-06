from Calculations.OneVelocity.OvAUSMplus import get_flux_bord


def get_x_v_left(l, tau, p=0):
    """
    Функция получения координаты и скорости левой границы
    :param p: давление с другой стороны границы
    :param l: слой по времени
    :param tau: шаг по времени
    :return: координату и скорость левой границы
    """
    V_l = round(l.V[0] + l.get_a(0, p) * tau, 8)
    x_l = round(l.x[0] + tau * l.V[0] + 0.5 * l.get_a(0, p) * tau * tau, 8)
    return x_l, V_l


def get_x_v_right(l, tau, p=0):
    """
    Функция получения координаты и скорости правой границы
    :param p: давление с другой стороны границы
    :param l: слой по времени
    :param tau: шаг по времени
    :return: координату и скорость правой границы
    """
    V_r = round(l.V[-1] + l.get_a(-1, p) * tau, 8)
    x_r = round(l.x[-1] + tau * l.V[-1] + 0.5 * l.get_a(-1, p) * tau * tau, 8)
    return x_r, V_r


def func_bord_left(r1, u1, p1, z1, V):
    """
    Функция для определения параметров в левой фиктивной ячейке
    :param r1: плотность в крайней левой ячейке
    :param u1: скорость в крайней левой ячейке
    :param p1: давление в крайней левой ячейке
    :param z1: толщина сгоревшего свода в крайней левой ячейке
    :param V: скорость левой границы
    :return:
    """
    r2 = r1
    u2 = -u1 + 2 * V
    p2 = p1
    z2 = z1
    return r2, u2, p2, z2


def func_bord_right(r1, u1, p1, z1, V):
    """
    Функция для определения параметров в правой фиктивной ячейке
    :param r1: плотность в крайней правой ячейке
    :param u1: скорость в крайней правой ячейке
    :param p1: давление в крайней правой ячейке
    :param z1: толщина сгоревшего свода в крайней правой ячейке
    :param V: скорость правой границы
    :return:
    """
    r2 = r1
    u2 = -u1 + 2 * V
    p2 = p1
    z2 = z1
    return r2, u2, p2, z2


def get_flux_left(l):
    """
    Фукнция для определения потока через левую границу сетки
    :param l: слой по времени
    :return:
    """
    return get_flux_bord(l, 0, func_bord_left)


def get_flux_right(l):
    """
    Фукнция для определения потока через правую границу сетки
    :param l: слой по времени
    :return:
    """
    return get_flux_bord(l, -1, func_bord_right)
