import csv
from typing import Tuple

import numpy as np
from matplotlib import pyplot as plt
from numpy import genfromtxt

# my_data = genfromtxt('my_file.csv', delimiter=',')

L = 0
N = 1
K = 2
QBER = 3
mean_tau_misses = 4
max_reps = 5
min_reps = 6
mean_reps = 7
median_reps = 8
std_dev = 9
var = 10


def get_data(filename: str) -> None:
    data = np.genfromtxt(filename, delimiter=';', skip_header=True)
    # L, N*K, QBER, TAU_MISS, MAX, MIN, MEAN, MEDIAN, STD_DEV, VAR
    data = [[row[0], row[1] * row[2], *row[3:]] for row in data]
    data.sort(key=lambda x: (x[0], x[2], x[1]))  # sorted by L, QBER than N*K

    for i in range(1, 6):
        for j in range(1, 12):
            l_3 = list(filter(lambda x: x[0] == i, data))  # only with L==3
            n_ks = [row[1] for row in l_3]
            y = [row[7] for row in l_3]
            # plt.scatter(n_ks, y)
            # plt.show()

            qber_8 = list(filter(lambda x: x[2] == j, l_3))  # only with QBER==8
            n_ks = [row[1] for row in qber_8]
            y = [row[7] for row in qber_8]
            # plt.scatter(n_ks, y)
            z = np.polyfit(n_ks, y, 9)
            p = np.poly1d(z)
            plt.plot(n_ks, p(n_ks), label=f'L={i}, QBER={j}')
        plt.show()
    # plt.show()
    # calculate equation for quadratic trendline
    # z = np.polyfit(n_ks, y, 2)
    # p = np.poly1d(z[0])
    #
    # # add trendline to plot
    # plt.plot(n_ks, p(n_ks))
    # # plt.show()

    print('OK')


get_data('../results/data_stats/stats_bursty.csv')