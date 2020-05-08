class ThermoLayer(object):
    def __init__(self, init_dict):
        self.init_dict = init_dict
        # Шаг по времени
        self.tau = init_dict['t_end'] / 100
        # Шаги по пространству
        self.n_x = init_dict['n_x']
        self.h_x = init_dict['L'] / (self.n_x - 1)
        self.n_r = init_dict['n_r']
        self.h_r = (init_dict['R'] - init_dict['r']) / (self.n_r - 1)
        self.r = [i * self.h_r for i in range(self.n_r)]
        # Константы для коэффициентов A, B, C, F трехточечного разностного уравнения
        self.lambd_h2_x = init_dict['param_material']['lambd'] / self.h_x ** 2
        self.lambd_h2_r = init_dict['param_material']['lambd'] / self.h_r ** 2
        self.lambd_rocp = init_dict['param_material']['ro'] * init_dict['param_material']['cp'] / self.tau
        # Начальное распределение температуры
        self.T = [[init_dict['T_0'] for j in range(self.n_r)] for i in range(self.n_x)]
        # Коэффициент температуропроводности
        self.a = init_dict['param_material']['lambd'] / (init_dict['param_material']['ro'] *
                                                         init_dict['param_material']['cp'])

    def left_bottom_board(self, i, numb_error=1, o_h=1, side='left'):
        '''
        Левая или нижняя границы для ошибок первого, второго и третьего рода (1 и 2-ого порядка точности)
        numb_error - номер рода ошибки,
        o_h - порядок точности,
        return alpha_0, beta_0 - коэффициенты прогонки у левой или нижней границы
        '''
        if side == 'left':
            h = self.h_x
            T = self.T[0][i]
        else:
            h = self.h_r
            T = self.T[i][0]

        if numb_error == 1:
            alpha_0 = 0
            if side == 'bottom':
                beta_0 = self.init_dict[f'T_{side}'][i]
            else:
                beta_0 = self.init_dict[f'T_{side}']
            return alpha_0, beta_0
        elif numb_error == 2:
            if o_h == 1:
                alpha_0 = 1
                beta_0 = h * self.init_dict[f'q_{side}'] / self.init_dict['param_material']['lambd']
                return alpha_0, beta_0
            elif o_h == 2:
                alpha_0 = 2 * self.a * self.tau / (h ** 2 + 2 * self.a * self.tau)
                beta_0 = (h ** 2 / (h ** 2 + 2 * self.a * self.tau) * T +
                          2 * self.a * self.tau * h * self.init_dict[f'q_{side}'] /
                          (self.init_dict['param_material']['lambd'] * (h ** 2 + 2 * self.a * self.tau)))
                return alpha_0, beta_0
        elif numb_error == 3:
            Bi = self.init_dict[f'kappa_{side}'] * h / self.init_dict['param_material']['lambd']
            alpha_0 = 2 * self.a * self.tau / (h ** 2 + 2 * self.a * self.tau * (1 + Bi))
            beta_0 = (h ** 2 / (h ** 2 + 2 * self.a * self.tau * (1 + Bi)) * T +
                      2 * self.a * self.tau * Bi * self.init_dict[f'Te_{side}'] /
                      (h ** 2 + 2 * self.a * self.tau * (1 + Bi)))
            return alpha_0, beta_0

    def right_up_bord(self, i, numb_error=1, o_h=1, side='right'):
        '''
        Правая или верхняя границы для ошибок первого, второго и третьего рода (1 и 2-ого порядка точности)
        numb_error - номер рода ошибки,
        o_h - порядок точности,
        return T - температуру на правой или верхней границе
        '''
        if side == 'right':
            h = self.h_x
            T = self.T[-1][i]
        else:
            h = self.h_r
            T = self.T[i][-1]

        if numb_error == 1:
            T = self.init_dict[f'T_{side}']
            return T
        elif numb_error == 2:
            if o_h == 1:
                T = (self.init_dict['param_material']['lambd'] * self.beta[-1] - h * self.init_dict[f'q_{side}'] /
                     self.init_dict['param_material']['lambd'] * (1 - self.alpha[-1]))
                return T
            elif o_h == 2:
                T = ((2 * self.a * self.tau * self.init_dict['param_material']['lambd'] * self.beta[-1] -
                      2 * self.a * self.tau * h * self.init_dict[f'q_{side}'] +
                      h ** 2 * self.init_dict['param_material']['lambd'] * T) /
                     (h ** 2 * self.init_dict['param_material']['lambd'] +
                      2 * self.a * self.tau * self.init_dict['param_material']['lambd'] * (1 - self.alpha[-1])))
                return T
        elif numb_error == 3:
            Bi = self.init_dict[f'kappa_{side}'] * h / self.init_dict['param_material']['lambd']
            if o_h == 1:
                T = (self.beta[-1] + Bi * self.init_dict[f'Te_{side}']) / (1 + Bi - self.alpha[-1])
                return T
            elif o_h == 2:
                T = ((h ** 2 * T + 2 * self.a * self.tau * (self.beta[-1] + Bi * self.init_dict[f'Te_{side}'])) /
                     (h ** 2 + 2 * self.a * self.tau * (1 + Bi - self.alpha[-1])))
                return T

    def TDMA(self, order_dict):
        '''Метод прогонки
        order_dict - словарь, содержащий род ошибки и порядок точности на границах,
        numb_error_left, numb_error_right - номер рода ошибки на левой и правой границе,
        o_h_left, o_h_right - порядок точности на левой и правой границе
        '''
        for j in range(self.n_r):
            alpha_0, beta_0 = self.left_bottom_board(j, order_dict['numb_error_left'], order_dict['o_h_left'], 'left')
            self.alpha = [alpha_0]
            self.beta = [beta_0]

            for i in range(1, self.n_x - 1):
                A = C = self.lambd_h2_x
                B = 2 * self.lambd_h2_x + self.lambd_rocp
                F = - self.lambd_rocp * self.T[i][j]

                self.alpha.append(A / (B - C * self.alpha[i - 1]))
                self.beta.append((C * self.beta[i - 1] - F) / (B - C * self.alpha[i - 1]))

            self.T[-1][j] = self.right_up_bord(j, order_dict['numb_error_right'], order_dict['o_h_right'], 'right')

            for i in reversed(range(self.n_x - 1)):
                self.T[i][j] = self.alpha[i] * self.T[i + 1][j] + self.beta[i]

        for i in range(1, self.n_x - 1):
            alpha_0, beta_0 = self.left_bottom_board(i, order_dict['numb_error_bottom'], order_dict['o_h_bottom'],
                                                     'bottom')
            self.alpha = [alpha_0]
            self.beta = [beta_0]

            for j in range(1, self.n_r - 1):
                A = self.lambd_h2_r * (self.r[j] + self.r[j + 1]) / (2 * self.r[j])
                C = self.lambd_h2_r * (self.r[j - 1] + self.r[j]) / (2 * self.r[j])
                B = self.lambd_h2_r * (self.r[j - 1] + 2 * self.r[j] + self.r[j + 1]) / \
                    (2 * self.r[j]) + self.lambd_rocp
                F = - self.lambd_rocp * self.T[i][j]

                self.alpha.append(A / (B - C * self.alpha[j - 1]))
                self.beta.append((C * self.beta[j - 1] - F) / (B - C * self.alpha[j - 1]))

            self.T[i][-1] = self.right_up_bord(i, order_dict['numb_error_up'], order_dict['o_h_up'], 'up')

            for j in reversed(range(self.n_r - 1)):
                self.T[i][j] = self.alpha[j] * self.T[i][j + 1] + self.beta[j]
