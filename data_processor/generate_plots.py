from typing import List
import numpy as np
from matplotlib import pyplot as plt

from data_processor.common import (
    QBERType,
    ColumnsDataStats,
    RANDOM_QBER_STATS_DATA_PATH,
    BURSTY_QBER_STATS_DATA_PATH,
    PATH_TO_PLOTS, RANDOM_QBER_DATA_PATH, BURSTY_QBER_DATA_PATH
)
from data_processor.prepare import sort_and_prepare_data


def plot_qber(data: List, expected_l: int, data_type: QBERType, plotted_column: ColumnsDataStats) -> None:
    TESTED_QBER = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}
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
    plt.savefig(f'{PATH_TO_PLOTS}/QBER_L_{expected_l}_{plot_type}_{data_type}.png')
    plt.savefig(f'{PATH_TO_PLOTS}/QBER_L_{expected_l}_{plot_type}_{data_type}.svg')
    plt.show()


def plot_l(data: List, expected_qber: int, data_type: QBERType, plotted_column: ColumnsDataStats) -> None:
    TESTED_L = {1, 2, 3, 4, 5}
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
    plt.savefig(f'{PATH_TO_PLOTS}/L_QBER_{expected_qber}_{plot_type}_{data_type}.svg')
    plt.show()


def plot_compare_type_of_errors(random_data: List, bursty_data: List, qber: int, l: int,
                                plotted_column: ColumnsDataStats) -> None:
    random_data = list(filter(lambda x: x[ColumnsDataStats.QBER] == qber, random_data))  # only with QBER
    random_data = list(filter(lambda x: x[ColumnsDataStats.L] == l, random_data))  # only with L

    bursty_data = list(filter(lambda x: x[ColumnsDataStats.QBER] == qber, bursty_data))  # only with QBER
    bursty_data = list(filter(lambda x: x[ColumnsDataStats.L] == l, bursty_data))  # only with L

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
    plt.savefig(f'{PATH_TO_PLOTS}/data_type_L_{l}_QBER_{qber}_{plot_type}.svg')
    plt.show()


def plot_l_impact_on_const_TPM(n: int, k: int, qber: int, data_type: QBERType):
    data_filename = RANDOM_QBER_DATA_PATH if data_type == QBERType.RANDOM else BURSTY_QBER_DATA_PATH
    data = np.genfromtxt(data_filename, delimiter=';', skip_header=True)
    data = list(filter(lambda x: x[1] == n, data))  # only with n
    data = list(filter(lambda x: x[2] == k, data))  # only with k
    data = list(filter(lambda x: x[3] == qber, data))  # only with qber
    data = np.array(data)
    data = np.unique(data, axis=0)

    constants = data[:, 0:4]
    values = data[:, -1]
    # Calculate mean and standard deviation for each group of constants
    unique_constants = np.unique(constants, axis=0)
    mean_values = []
    std_deviations = []

    for const_group in unique_constants:
        mask = np.all(constants == const_group, axis=1)
        values_group = values[mask]
        mean_values.append(np.mean(values_group))
        std_deviations.append(np.std(values_group))

    # Convert lists to numpy arrays
    mean_values = np.array(mean_values)
    std_deviations = np.array(std_deviations)

    # Create the plot
    plt.figure()
    plt.errorbar(range(1, len(mean_values)+1), mean_values, yerr=std_deviations, fmt='o')

    plt.xticks(range(1, len(unique_constants)+1), range(1, len(unique_constants)+1))
    plt.xlabel('L')
    plt.ylabel('Mean required repetitions')
    plt.title(f'L influence on required number of repetition for constant TPM \n (N={n}, K={k}, QBER={qber})', wrap=True)
    plt.grid(True)

    plt.savefig(f'{PATH_TO_PLOTS}/l_impact_on_{data_type}_TPM_N_{n}_K_{k}_qber_{qber}.png')
    plt.savefig(f'{PATH_TO_PLOTS}/l_impact_on_{data_type}_TPM_N_{n}_K_{k}_qber_{qber}.svg')
    # Show the plot
    plt.show()


def plot_qber_impact_on_const_TPM(l: int, n: int, k: int, data_type: QBERType):
    data_filename = RANDOM_QBER_DATA_PATH if data_type == QBERType.RANDOM else BURSTY_QBER_DATA_PATH
    data = np.genfromtxt(data_filename, delimiter=';', skip_header=True)
    data = list(filter(lambda x: x[1] == n, data))  # only with n
    data = list(filter(lambda x: x[2] == k, data))  # only with k
    data = list(filter(lambda x: x[0] == l, data))  # only with l
    data = np.array(data)
    data = np.unique(data, axis=0)

    constants = data[:, 0:4]
    values = data[:, -1]
    # Calculate mean and standard deviation for each group of constants
    unique_constants = np.unique(constants, axis=0)
    mean_values = []
    std_deviations = []

    for const_group in unique_constants:
        mask = np.all(constants == const_group, axis=1)
        values_group = values[mask]
        mean_values.append(np.mean(values_group))
        std_deviations.append(np.std(values_group))

    # Convert lists to numpy arrays
    mean_values = np.array(mean_values)
    std_deviations = np.array(std_deviations)

    # Create the plot
    plt.figure()
    plt.errorbar(range(1, len(mean_values)+1), mean_values, yerr=std_deviations, fmt='o')

    plt.xticks(range(1, len(unique_constants)+1), range(1, len(unique_constants)+1))
    plt.xlabel('QBER [%]')
    plt.ylabel('Mean required repetitions')
    plt.title(f'QBER influence on required number of repetition for constant TPM \n (N={n}, K={k}, L={l})', wrap=True)
    plt.grid(True)

    plt.savefig(f'{PATH_TO_PLOTS}/qber_impact_on_{data_type}_TPM_N_{n}_K_{k}_L_{l}.png')
    plt.savefig(f'{PATH_TO_PLOTS}/qber_impact_on_{data_type}_TPM_N_{n}_K_{k}_L_{l}.svg')
    # Show the plot
    plt.show()


if __name__ == '__main__':
    sorted_bursty_data = sort_and_prepare_data(BURSTY_QBER_STATS_DATA_PATH)
    sorted_random_data = sort_and_prepare_data(RANDOM_QBER_STATS_DATA_PATH)

    for required_l in [1, 2, 3, 4, 5]:
        plot_qber(sorted_bursty_data, required_l, QBERType.BURSTY, ColumnsDataStats.REPS_MEAN)
        plot_qber(sorted_bursty_data, required_l, QBERType.BURSTY, ColumnsDataStats.MEAN_TAU_MISSED)
        plot_qber(sorted_random_data, required_l, QBERType.RANDOM, ColumnsDataStats.REPS_MEAN)
        plot_qber(sorted_random_data, required_l, QBERType.RANDOM, ColumnsDataStats.MEAN_TAU_MISSED)

    for required_qber in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
        plot_l(sorted_bursty_data, required_qber, QBERType.BURSTY, ColumnsDataStats.REPS_MEAN)
        plot_l(sorted_bursty_data, required_qber, QBERType.BURSTY, ColumnsDataStats.MEAN_TAU_MISSED)
        plot_l(sorted_random_data, required_qber, QBERType.RANDOM, ColumnsDataStats.REPS_MEAN)
        plot_l(sorted_random_data, required_qber, QBERType.RANDOM, ColumnsDataStats.MEAN_TAU_MISSED)

    plot_compare_type_of_errors(sorted_random_data, sorted_bursty_data, 9, 5, ColumnsDataStats.MEAN_TAU_MISSED)
    plot_compare_type_of_errors(sorted_random_data, sorted_bursty_data, 9, 5, ColumnsDataStats.REPS_MEAN)

    plot_l_impact_on_const_TPM(120, 110, 11, QBERType.RANDOM)
    plot_l_impact_on_const_TPM(120, 110, 11, QBERType.BURSTY)

    plot_qber_impact_on_const_TPM(4, 120, 110, QBERType.BURSTY)
    plot_qber_impact_on_const_TPM(4, 120, 110, QBERType.RANDOM)

# L and QBER influence on number of repetitions - DONE
# L and QBER influence on number of re-runs :) - DONE

# compare error type on repetitions for L = 5 and QBER = 9 - DONE
# compare error type on re-runs for L = 5 and QBER = 9 - DONE

# lets see for N on X axis
# lets see for K on X axis
