import time

from Calculations.Invariants.Plot import *
from Calculations.Pneum.PnInit import pn_create_layer


def solver(q, x_bord, geom, gas, T, p, n_cells, Ku, sigma_v, R, r):
    """
    Формирование словаря входных данных для расчета внутренней баллистики (газ)
    :param q: масса снаряда
    :param x_bord: координата x правой границы камеры сгорания
    :param geom: список кортежей из координаты узла и диаметра
    :param gas: словарь с характеристиками газа
    :param T: начальная температура в камере
    :param p: начальное давление в камере
    :param n_cells: кол-во узлов рассчетной сетки
    :param Ku: число Куранта
    :param sigma_v: предел упругости материала
    :param R: внешний радиус трубы (ствола)
    :param r: внутренний радиус трубы (ствола)
    :return: словарь входных данных
    """
    return {'borders': [{'m': 1000, 'p_f': 1e8, 'x': 0, 'V': 0},
                        {'m': q, 'p_f': 101325, 'x': x_bord, 'V': 0}],
            'geom': geom,
            'grids': [{'consts': gas,
                       'init_const': {'T': T, 'p': p},
                       'n_cells': n_cells,
                       'name': 'gas',
                       'type': 'gas'}],
            'sigma_v': sigma_v,
            'R': R,
            'r': r,
            'courant_number': Ku}


def calc_run(solver):
    """
    Функция для рассчета внутренней баллистики (газ)
    :param solver: словарь входных данных
    :return: массив распределения температуры после вылета снаряда из ствола
    """
    start_time = time.time()

    layer = pn_create_layer(solver)

    time_arr = [0]              # Список времени для графика
    V_arr = [0]                 # Список скорости для графика
    x_arr = [layer.x[-1]]           # Список координаты для графика
    p_arr_sn = [layer.p[-1]]
    p_arr_dn = [layer.p[0]]
    Vmax = 0

    flag = True

    results = [solver]

    while True:
        if (solver['geom'][-1][0] - layer.x[-1]) <= 0.001:
            results.append({'time_arr': time_arr,
                            'V_arr': V_arr,
                            'x_arr': x_arr,
                            'p_arr_sn': p_arr_sn,
                            'p_arr_dn': p_arr_dn})

            break
        if (Vmax - layer.V[-1]) > 1:
            flag = False
            print('Замедляется')
            break

        sigma = 2 / 3 * layer.p * (2 * layer.R_out ** 2 + layer.r_in ** 2) / (layer.R_out ** 2 - layer.r_in ** 2)

        if sum(layer.sigma_v >= sigma) != layer.n:
            flag = False
            print('Не соблюдается условие прочности! Превышен предел упругости материала!')
            break

        tau = solver['courant_number'] * layer.time_step() # Вычисление шага по времени
        layer1 = layer.euler_step(layer, tau)
        layer = layer1

        time_arr.append(layer.time)         # Добавление текущего шага по времени в список для графика
        V_arr.append(layer.V[-1])           # Добавление текущей скорости поршня в список для графика
        x_arr.append(layer.x[-1])           # Добавление текущей координаты поршня в список для графика
        p_arr_sn.append(layer.p[-1])
        p_arr_dn.append(layer.p[0])

        if layer.V[-1] > Vmax:
            Vmax = layer.V[-1]

    if flag:
        T = layer.p * (1 / layer.q[0] - layer.covolume) / layer.R_const

        # print('Расчет закончен')
        # print("--- %s seconds ---" % (time.time() - start_time))
        #
        # print('Условие прочности соблюдается!')
        # print('Время вылета:', time_arr[-1], 'с')
        # print('Скорость вылета:', V_arr[-1], 'м/с')
        #
        # plot_one(time_arr, V_arr, 'График скорости снаряда от времени', 'Время', 'Скорость')
        # plot_one(x_arr, V_arr, 'График скорости снаряда от времени', 'Координата', 'Скорость')
        # plot_one(time_arr, p_arr_sn, 'График давления на дно снаряда от времени', 'Время', 'Давление')
        # plot_one(time_arr, p_arr_dn, 'График давления на дно ствола от времени', 'Время', 'Давление')

        return results, T, True
    else:
        return None, None, False
