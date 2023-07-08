from typing import List

import numpy as np
from matplotlib import pyplot as plt

L = 0
N_K = 1
QBER = 2
mean_tau_misses = 3
max_reps = 4
min_reps = 5
mean_reps = 6
median_reps = 7
std_dev = 8
var = 9


def sort_and_prepare_data(filename: str) -> List[List[float]]:
    data = np.genfromtxt(filename, delimiter=';', skip_header=True)
    # L, N*K, QBER, TAU_MISS, MAX, MIN, MEAN, MEDIAN, STD_DEV, VAR
    data = [[row[0], row[1] * row[2], *row[3:]] for row in data]
    data.sort(key=lambda x: (x[L], x[QBER], x[N_K]))  # sorted by L, QBER than N*K
    return data


def plot_qber(data: List, expected_l: int, expected_QBER: List[int]) -> None:
    data = list(filter(lambda x: x[L] == expected_l, data))  # only with L==expected_l
    for qber in expected_QBER:
        qber_data = list(filter(lambda x: x[QBER] == qber, data))  # only with QBER
        x = [row[N_K] for row in qber_data]
        y = [row[mean_reps] for row in qber_data]
        z = np.polyfit(x, y, 9)
        p = np.poly1d(z)
        plt.plot(x, p(x), label=f'QBER: {qber}')
    plt.title(f'QBER influence on mean number of required repetitions of TMP with L={expected_l}')
    plt.xlabel(f'Number of input neurons multiplied by number of hidden neurons [N*K]')
    plt.ylabel(f'Mean number of required repetitions of TMP')
    plt.legend()
    plt.show()


def plot_l(data: List, expected_qber: int, expected_l: List[int]) -> None:
    data = list(filter(lambda x: x[QBER] == expected_qber, data))  # only with QBER

    for l in expected_l:
        l_data = list(filter(lambda x: x[L] == l, data))  # only with L==expected_l
        x = [row[N_K] for row in l_data]
        y = [row[mean_reps] for row in l_data]
        z = np.polyfit(x, y, 9)
        p = np.poly1d(z)
        plt.plot(x, p(x), label=f'L: {l}')
    plt.title(f'L influence on mean number of required repetitions of TMP with QBER={expected_qber}')
    plt.xlabel(f'Number of input neurons multiplied by number of hidden neurons [N*K]')
    plt.ylabel(f'Mean number of required repetitions of TMP')
    plt.legend()
    plt.show()



if __name__ == '__main__':
    bursty_data = '../results/data_stats/stats_bursty.csv'
    random_data = '../results/data_stats/stats_random.csv'
    sorted_bursty_data = sort_and_prepare_data(bursty_data)
    sorted_random_data = sort_and_prepare_data(random_data)

    for required_l in [1,2,3,4,5]:
        plot_qber(sorted_bursty_data, required_l, [1,2,3,4,5,6,7,8,9,10,11])
        plot_qber(sorted_random_data, required_l, [1,2,3,4,5,6,7,8,9,10,11])

    for required_qber in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
        plot_l(sorted_bursty_data, required_qber, [1,2,3,4,5])
        plot_l(sorted_random_data,required_qber, [1,2,3,4,5])
