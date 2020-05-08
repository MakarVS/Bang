import time
import numpy as np

from Calculations.OneVelocity.OvInit import ov_create_layer
from Calculations.Invariants.WriteToJson import write_to_file
from Calculations.Invariants.Plot import plot_one

# !!!!!!!!!!!!!!!!!!!!!!!! РАБОЧАЯ ПРОГРАММА !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


def solver(q, p_f, x_bord, geom, powder, omega, n_cells, Ku, sigma_v, R, r):
    return {'borders': [{'m': 1000, 'p_f': 1e8, 'x': 0, 'V': 0},
                        {'m': q, 'p_f': p_f, 'x': x_bord, 'V': 0}],
            'geom': geom,
            'grids': [{'consts': powder,
                       'init_const': {'omega': omega,
                                      't_init': 0},
                       'n_cells': n_cells,
                       'name': 'powder',
                       'type': 'powder'}],
            'q': q,
            'sigma_v': sigma_v,
            'R': R,
            'r': r,
            'courant_number': Ku}


def calc_run(solver):
    start_time = time.time()
    layer = ov_create_layer(solver)

    time_arr = [0]  # Список времени для графика
    V_arr = [0]  # Список скорости для графика
    x_arr = [layer.x[-1]]  # Список координаты для графика
    p_arr_sn = [layer.p[-1]]
    p_arr_dn = [layer.p[0]]
    Vmax = 0

    results = [solver]

    while True:
        if (solver['geom'][-1][0] - layer.x[-1]) <= 0.001:
            results.append({'time_arr': time_arr,
                            'V_arr': V_arr,
                            'x_arr': x_arr,
                            'p_arr_sn': p_arr_sn,
                            'p_arr_dn': p_arr_dn})

            # write_to_file(results, solver['number'])
            break

        if (Vmax - layer.V[-1]) > 1:
            break

        sigma = 2 / 3 * layer.p * (2 * layer.R_out ** 2 + layer.r_in ** 2) / (layer.R_out ** 2 - layer.r_in ** 2)

        if sum(layer.sigma_v >= sigma) != layer.n:
            print('Не соблюдается условие прочности! Превышен предел упругости материала!')
            break

        tau = solver['courant_number'] * layer.time_step()  # Вычисление шага по времени
        layer1 = layer.euler_step(layer, tau)
        layer = layer1

        time_arr.append(layer.time)  # Добавление текущего шага по времени в список для графика
        V_arr.append(layer.V[-1])  # Добавление текущей скорости поршня в список для графика
        x_arr.append(layer.x[-1])  # Добавление текущей координаты поршня в список для графика
        p_arr_sn.append(layer.p[-1])
        p_arr_dn.append(layer.p[0])

        if layer.V[-1] > Vmax:
            Vmax = layer.V[-1]

    T = layer.powd.etta * (layer.q[2] / layer.q[0] - 0.5 * np.square(layer.q[1] / layer.q[0])) \
        / (layer.powd.f / layer.powd.T_1)

    print("--- %s seconds ---" % (time.time() - start_time))

    print('Условие прочности соблюдается!')
    print('Время вылета:', time_arr[-1], 'с')
    print('Скорость вылета:', V_arr[-1], 'м/с')
    print(T)

    plot_one(time_arr, V_arr, 'График скорости снаряда от времени', 'Время', 'Скорость')
    plot_one(x_arr, V_arr, 'График скорости снаряда от времени', 'Координата', 'Скорость')
    plot_one(time_arr, p_arr_sn, 'График давления на дно снаряда от времени', 'Время', 'Давление')
    plot_one(time_arr, p_arr_dn, 'График давления на дно снаряда от времени', 'Время', 'Давление')

    return T
