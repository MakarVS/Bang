import math


def equation_of_motion(V1, p, d, delta_l, q, cut_param):
    S = math.pi * pow(d, 2) / 4
    alpha = math.radians(cut_param['alpha'])
    V2 = V1 - (p * S * delta_l * (1 + cut_param['lambd'] * (pow(math.tan(alpha), 2) + cut_param['nu'] *
                                                            math.tan(alpha)))) / (q * V1)
    # V2 = V1 - p * S * delta_l / q * V1
    return V2