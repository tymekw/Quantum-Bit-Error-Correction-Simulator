import csv
from dataclasses import dataclass
from typing import Tuple

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

TRAINING_DATASET_FILENAME = 'simulator/whole_results_10_140.csv'
TESTING_DATASET_FILENAME = 'simulator/whole_results_test_10_140.csv'
PREPARED_DATA_FILENAME = 'prepared_data'
PREPARED_DATA_HEADER = ['L;N;K;QBER;REPETITIONS']


@dataclass
class QBERType:
    RANDOM = 'random'
    BURSTY = 'bursty'

def write_prepared_data(path: str, is_test_data: bool=False) -> None:
    with open(path, 'r') as file:
        reader = csv.reader(file,  delimiter =';')
        prepared_data_random_qber_filename = ('test_' if is_test_data else '') + \
                                             PREPARED_DATA_FILENAME + '_' + QBERType.RANDOM + '.csv'
        prepared_data_bursty_qber_filename = ('test_' if is_test_data else '') + \
                                             PREPARED_DATA_FILENAME + '_' + QBERType.BURSTY + '.csv'

        with open(prepared_data_random_qber_filename, 'w', newline='') as random_qber_file,\
                open(prepared_data_bursty_qber_filename, 'w',  newline='') as bursty_qber_file:
                    random_qber_writer = csv.writer(random_qber_file)
                    bursty_qber_writer = csv.writer(bursty_qber_file)
                    random_qber_writer.writerow(PREPARED_DATA_HEADER)
                    bursty_qber_writer.writerow(PREPARED_DATA_HEADER)
                    next(reader, None) # skip header
                    for row in reader:
                        required_data = [*row[0:4], row[-1]]
                        if row[5] == QBERType.RANDOM:
                            random_qber_writer.writerow(required_data)
                        elif row[5] == QBERType.BURSTY:
                            bursty_qber_writer.writerow(required_data)

def get_observations_and_targets(filename: str) -> Tuple[np.array, np.array]:
    with open(filename, 'r') as data_file:
        reader = csv.reader(data_file)
        next(reader, None) # skip header
        observations = []
        targets = []
        for row in reader:
            observations.append([int(i) for i in row[:-1]])
            targets.append(int(row[-1]))

    return np.array(observations), np.array(targets)


if __name__ == '__main__':
    write_prepared_data(TRAINING_DATASET_FILENAME, is_test_data=False)
    write_prepared_data(TESTING_DATASET_FILENAME, is_test_data=True)
    X, Y = get_observations_and_targets(PREPARED_DATA_FILENAME + '_' + QBERType.RANDOM + '.csv')
    X_test, Y_test = get_observations_and_targets('test_' + PREPARED_DATA_FILENAME + '_' + QBERType.RANDOM + '.csv')
    linear_regression = LinearRegression().fit(X, Y)
    Y_pred = linear_regression.predict(X_test)
    print("Mean squared error: %.2f" % mean_squared_error(Y_test, Y_pred))
    print("Coefficient of determination: %.2f" % r2_score(Y_test, Y_pred))



