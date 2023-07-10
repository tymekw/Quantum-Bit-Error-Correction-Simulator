from typing import List
import numpy as np
from matplotlib import pyplot as plt

from neural_crypto.data_processor.common import (
    QBERType,
    ColumnsDataStats,
    RANDOM_QBER_STATS_DATA_PATH,
    BURSTY_QBER_STATS_DATA_PATH,
    PATH_TO_PLOTS
)
from neural_crypto.data_processor.prepare import sort_and_prepare_data


def plot_qber(data: List, expected_l: int, data_type: QBERType, plotted_column: ColumnsDataStats) -> None:
    TESTED_QBER = {1,2,3,4,5,6,7,8,9,10,11}
    data = list(filter(lambda x: x[ColumnsDataStats.L] == expected_l, data))  # only with L==expected_l

    for qber in TESTED_QBER:
        qber_data = list(filter(lambda x: x[ColumnsDataStats.QBER] == qber, data))  # only with QBER
        x = [row[ColumnsDataStats.N_K] for row in qber_data]
        y = [row[plotted_column] for row in qber_data]
        z = np.polyfit(x, y, 9)
        p = np.poly1d(z)
        plt.plot(x, p(x), label=f'QBER: {qber}')

    plot_type = 'repetitions' if plotted_column == ColumnsDataStats.REPS_MEAN else 're-runs'
    title = f'QBER influence on mean number of required {plot_type} of TPM with L={expected_l}'
    plt.title(title, wrap=True)
    plt.xlabel(f'Number of input neurons multiplied by number of hidden neurons [N*K]')
    plt.ylabel(f'Mean number of required repetitions of TPM')
    plt.legend()
    plt.savefig(f'../results/plots/QBER_L_{expected_l}_{plot_type}_{data_type}.png')
    plt.show()


def plot_l(data: List, expected_qber: int, data_type: QBERType, plotted_column: ColumnsDataStats) -> None:
    TESTED_L = {1,2,3,4,5}
    data = list(filter(lambda x: x[ColumnsDataStats.QBER] == expected_qber, data))  # only with QBER

    for l in TESTED_L:
        l_data = list(filter(lambda x: x[ColumnsDataStats.L] == l, data))  # only with L==expected_l
        x = [row[ColumnsDataStats.N_K] for row in l_data]
        y = [row[plotted_column] for row in l_data]
        z = np.polyfit(x, y, 9)
        p = np.poly1d(z)
        plt.plot(x, p(x), label=f'L: {l}')
    plot_type = 'repetitions' if plotted_column == ColumnsDataStats.REPS_MEAN else 're-runs'
    title = f'L influence on mean number of required {plot_type} of TPM with {data_type} QBER={expected_qber}'
    plt.title(title, wrap=True)
    plt.xlabel(f'Number of input neurons multiplied by number of hidden neurons [N*K]')
    plt.ylabel(f'Mean number of required repetitions of TPM')
    plt.legend()
    plt.savefig(f'{PATH_TO_PLOTS}/L_QBER_{expected_qber}_{plot_type}_{data_type}.png')
    plt.show()

def plot_compare_type_of_errors(random_data: List, bursty_data: List, qber: int, l: int, plotted_column: ColumnsDataStats) -> None:
    random_data = list(filter(lambda x: x[ColumnsDataStats.QBER] == qber, random_data))  # only with QBER
    random_data = list(filter(lambda x: x[ColumnsDataStats.L] == l, random_data)) # only with L

    bursty_data = list(filter(lambda x: x[ColumnsDataStats.QBER] == qber, bursty_data))  # only with QBER
    bursty_data = list(filter(lambda x: x[ColumnsDataStats.L] == l, bursty_data)) # only with L

    for data in (random_data, bursty_data):
        x = [row[ColumnsDataStats.N_K] for row in data]
        y = [row[plotted_column] for row in data]
        z = np.polyfit(x, y, 9)
        p = np.poly1d(z)
        label = 'random errors' if data == random_data else 'bursty errors'
        plt.plot(x, p(x), label=label)

    plot_type = 'repetitions' if plotted_column == ColumnsDataStats.REPS_MEAN else 're-runs'
    title = f'Errors type influence on mean number of required {plot_type} of TPM with QBER={qber} and L={l}'
    plt.title(title, wrap=True)
    plt.xlabel(f'Number of input neurons multiplied by number of hidden neurons [N*K]')
    plt.ylabel(f'Mean number of required repetitions of TPM')
    plt.legend()
    plt.savefig(f'{PATH_TO_PLOTS}/data_type_L_{l}_QBER_{qber}_{plot_type}.png')
    plt.show()


if __name__ == '__main__':
    sorted_bursty_data = sort_and_prepare_data(BURSTY_QBER_STATS_DATA_PATH)
    sorted_random_data = sort_and_prepare_data(RANDOM_QBER_STATS_DATA_PATH)

    # TODO
    # whole_random_data = '../results/data_whole/data_random.csv'
    # sorted_random_data_whole = sort_and_prepare_data(whole_random_data)

    for required_l in [1,2,3,4,5]:
        plot_qber(sorted_bursty_data, required_l, QBERType.BURSTY, ColumnsDataStats.REPS_MEAN)
        plot_qber(sorted_bursty_data, required_l, QBERType.BURSTY, ColumnsDataStats.MEAN_TAU_MISSED)
        plot_qber(sorted_random_data, required_l, QBERType.RANDOM, ColumnsDataStats.REPS_MEAN)
        plot_qber(sorted_random_data, required_l, QBERType.RANDOM, ColumnsDataStats.MEAN_TAU_MISSED)

    for required_qber in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
        plot_l(sorted_bursty_data, required_qber, QBERType.BURSTY, ColumnsDataStats.REPS_MEAN)
        plot_l(sorted_bursty_data, required_qber, QBERType.BURSTY, ColumnsDataStats.MEAN_TAU_MISSED)
        plot_l(sorted_random_data,required_qber, QBERType.RANDOM, ColumnsDataStats.REPS_MEAN)
        plot_l(sorted_random_data,required_qber, QBERType.RANDOM, ColumnsDataStats.MEAN_TAU_MISSED)

    plot_compare_type_of_errors(sorted_random_data, sorted_bursty_data, 9, 5, ColumnsDataStats.MEAN_TAU_MISSED)
    plot_compare_type_of_errors(sorted_random_data, sorted_bursty_data, 9, 5, ColumnsDataStats.REPS_MEAN)


# L and QBER influence on number of repetitions - DONE
# L and QBER influence on number of re-runs :) - DONE

# compare error type on repetitions for L = 5 and QBER = 9 - DONE
# compare error type on re-runs for L = 5 and QBER = 9 - DONE

# lets see for N on X axis
# lets see for K on X axis

