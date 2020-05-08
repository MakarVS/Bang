from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

from Calculations.HeatTransfer.ThermoLayer import ThermoLayer


def solver_thermo(ro, cp, lambd, n_x, n_r, L, R, r, t_end, T_env, T_in):
    return {'param_material': {'ro': ro,
                               'cp': cp,
                               'lambd': lambd},
            'T_0': T_env,
            'n_x': n_x,
            'n_r': n_r,
            'L': L,
            'R': R,
            'r': r,
            't_end': t_end,
            'T_up': T_env,
            'T_right': T_env,
            'T_bottom': T_in,
            'T_left': 20
            }


def order_solver():
    return {'numb_error_left': 1,
            'numb_error_right': 1,
            'o_h_left': 1,
            'o_h_right': 1,
            'numb_error_bottom': 1,
            'numb_error_up': 1,
            'o_h_bottom': 1,
            'o_h_up': 1
            }


def calc_run(solver, order=order_solver()):
    time = 0
    layer_cil = ThermoLayer(solver)

    while time <= solver['t_end']:
        time += layer_cil.tau
        layer_cil.TDMA(order)

    r = [round((solver['r'] + layer_cil.h_r * i) * 1000, 2) for i in range(solver['n_r'] - 1, -1, -1)]
    l = [round(layer_cil.h_x * i * 1000, 2) for i in range(solver['n_x'])]

    data_result = pd.DataFrame(np.rot90(layer_cil.T, 1), columns=l, index=r)
    fig, ax = plt.subplots(figsize=(20, 3))
    heatmap_plot = sns.heatmap(data_result, ax=ax, robust=True, cmap=sns.diverging_palette(240, 10, n=9))
    plt.show()
