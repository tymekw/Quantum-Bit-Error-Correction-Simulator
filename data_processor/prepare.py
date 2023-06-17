import csv

import numpy as np

from neural_crypto.data_processor.common import (
    RANDOM_QBER_TEST_DATA_PATH,
    RANDOM_QBER_DATA_PATH,
    BURSTY_QBER_TEST_DATA_PATH,
    BURSTY_QBER_DATA_PATH,
    PREPARED_DATA_HEADER,
    QBERType,
    RAW_TESTING_DATASET_PATH,
    RAW_TRAINING_DATASET_PATH,
    STATS_DATA_HEADER,
    RANDOM_QBER_TEST_STATS_DATA_PATH,
    BURSTY_QBER_TEST_STATS_DATA_PATH,
    RANDOM_QBER_STATS_DATA_PATH,
    BURSTY_QBER_STATS_DATA_PATH,
)

def write_prepared_data(path: str, is_test_data: bool=False) -> None:
    with open(path, 'r') as file:
        reader = csv.reader(file,  delimiter =';')
        prepared_data_random_qber_filename = RANDOM_QBER_TEST_DATA_PATH if is_test_data else RANDOM_QBER_DATA_PATH
        prepared_data_bursty_qber_filename = BURSTY_QBER_TEST_DATA_PATH if is_test_data else BURSTY_QBER_DATA_PATH

        with open(prepared_data_random_qber_filename, 'w+', newline='') as random_qber_file,\
                open(prepared_data_bursty_qber_filename, 'w+',  newline='') as bursty_qber_file:
                    random_qber_writer = csv.writer(random_qber_file, delimiter =';')
                    bursty_qber_writer = csv.writer(bursty_qber_file, delimiter =';')
                    random_qber_writer.writerow(PREPARED_DATA_HEADER)
                    bursty_qber_writer.writerow(PREPARED_DATA_HEADER)
                    next(reader, None) # skip header
                    for row in reader:
                        required_data = [*row[0:4], row[-1]]
                        if row[5] == QBERType.RANDOM:
                            random_qber_writer.writerow(required_data)
                        elif row[5] == QBERType.BURSTY:
                            bursty_qber_writer.writerow(required_data)

def write_prepared_data_with_statistics(path: str, path_to_write: str) -> None:
    with open(path, 'r') as file:
        reader = csv.reader(file, delimiter =';')

        is_next = next(reader, None)
        with open(path_to_write, 'w+', newline='') as stats_file:
            stats_writer = csv.writer(stats_file, delimiter =';')
            stats_writer.writerow(STATS_DATA_HEADER)
            while is_next:
                rows = [next(reader, None) for _ in range(6)]
                is_next = None not in rows
                if is_next:
                    REPS = [int(row[-1]) for row in rows]
                    max_reps = str(max(REPS))
                    min_reps = str(min(REPS))
                    mean = str(int(np.mean(REPS)))
                    median = str(int(np.median(REPS)))
                    std_dev = str(np.std(REPS))
                    variance = str(np.var(REPS))
                    row_with_stats = rows[0][0:4] + [max_reps, min_reps, mean, median, std_dev, variance]
                    stats_writer.writerow(row_with_stats)



if __name__ == '__main__':
    write_prepared_data(RAW_TRAINING_DATASET_PATH, is_test_data=False)
    write_prepared_data(RAW_TESTING_DATASET_PATH, is_test_data=True)
    write_prepared_data_with_statistics(RANDOM_QBER_DATA_PATH, RANDOM_QBER_STATS_DATA_PATH)
    write_prepared_data_with_statistics(BURSTY_QBER_DATA_PATH, BURSTY_QBER_STATS_DATA_PATH)
    write_prepared_data_with_statistics(RANDOM_QBER_TEST_DATA_PATH, RANDOM_QBER_TEST_STATS_DATA_PATH)
    write_prepared_data_with_statistics(BURSTY_QBER_TEST_DATA_PATH, BURSTY_QBER_TEST_STATS_DATA_PATH)
