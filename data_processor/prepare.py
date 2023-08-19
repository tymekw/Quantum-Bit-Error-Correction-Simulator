import csv
from typing import List

import numpy as np

from data_processor.common import (
    RANDOM_QBER_DATA_PATH,
    BURSTY_QBER_DATA_PATH,
    PREPARED_DATA_HEADER,
    QBERType,
    STATS_DATA_HEADER,
    RANDOM_QBER_STATS_DATA_PATH,
    BURSTY_QBER_STATS_DATA_PATH,
    RAW_DATASET_PATH,
    ColumnsDataStats, RANDOM_QBER_DATA_PATH_EVE, BURSTY_QBER_DATA_PATH_EVE, PREPARED_DATA_HEADER_EVE,
    RAW_DATASET_PATH_EVE,
)


def write_prepared_data(path: str) -> None:
    with open(path, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        prepared_data_random_qber_filename = RANDOM_QBER_DATA_PATH_EVE
        prepared_data_bursty_qber_filename = BURSTY_QBER_DATA_PATH_EVE

        with open(prepared_data_random_qber_filename, 'w+', newline='') as random_qber_file, \
                open(prepared_data_bursty_qber_filename, 'w+', newline='') as bursty_qber_file:
            random_qber_writer = csv.writer(random_qber_file, delimiter=';')
            bursty_qber_writer = csv.writer(bursty_qber_file, delimiter=';')
            random_qber_writer.writerow(PREPARED_DATA_HEADER_EVE)
            bursty_qber_writer.writerow(PREPARED_DATA_HEADER_EVE)
            next(reader, None)  # skip header
            for row in reader:
                # required_data = [*row[0:4], row[7], row[-1:]]
                required_data_eve = [*row[0:4], row[7], *row[-3:]]
                if row[5] == QBERType.RANDOM:
                    random_qber_writer.writerow(required_data_eve)
                elif row[5] == QBERType.BURSTY:
                    bursty_qber_writer.writerow(required_data_eve)


def write_prepared_data_with_statistics(path: str, path_to_write: str) -> None:
    with open(path, 'r') as file:
        reader = csv.reader(file, delimiter=';')

        is_next = next(reader, None)
        with open(path_to_write, 'w+', newline='') as stats_file:
            stats_writer = csv.writer(stats_file, delimiter=';')
            stats_writer.writerow(STATS_DATA_HEADER)
            while is_next:
                rows = [next(reader, None) for _ in range(6)]
                is_next = None not in rows
                if is_next:
                    mean_tau_misses = str(int(np.mean([int(row[-2]) for row in rows])))
                    REPS = [int(row[-1]) for row in rows]
                    max_reps = str(max(REPS))
                    min_reps = str(min(REPS))
                    mean = str(int(np.mean(REPS)))
                    median = str(int(np.median(REPS)))
                    std_dev = str(np.std(REPS))
                    variance = str(np.var(REPS))
                    row_with_stats = rows[0][0:4] + [mean_tau_misses, max_reps, min_reps, mean, median, std_dev,
                                                     variance]
                    stats_writer.writerow(row_with_stats)


def sort_and_prepare_data(filename: str) -> List[List[float]]:
    data = np.genfromtxt(filename, delimiter=';', skip_header=True)
    # L, N*K, QBER, TAU_MISS, MAX, MIN, MEAN, MEDIAN, STD_DEV, VAR
    data = [[row[0], row[1] * row[2], *row[3:]] for row in data]
    data.sort(key=lambda x: (
    x[ColumnsDataStats.L], x[ColumnsDataStats.QBER], x[ColumnsDataStats.N_K]))  # sorted by L, QBER than N*K
    return data


if __name__ == '__main__':
    # write_prepared_data(RAW_DATASET_PATH)
    # write_prepared_data_with_statistics(RANDOM_QBER_DATA_PATH, RANDOM_QBER_STATS_DATA_PATH)
    # write_prepared_data_with_statistics(BURSTY_QBER_DATA_PATH, BURSTY_QBER_STATS_DATA_PATH)
    write_prepared_data(RAW_DATASET_PATH_EVE)


