import csv
from typing import Tuple, Any

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

from neural_crypto.data_processor.common import (
    RANDOM_QBER_DATA_PATH,
    RANDOM_QBER_TEST_DATA_PATH,
    BURSTY_QBER_DATA_PATH,
    BURSTY_QBER_TEST_DATA_PATH,
)


def get_all_observations_and_targets(filename: str) -> Tuple[np.array, np.array]:
    with open(filename, 'r') as data_file:
        reader = csv.reader(data_file)
        next(reader, None) # skip header
        observations = []
        targets = []
        for row in reader:
            observations.append([int(i) for i in row[:-1]])
            targets.append(int(row[-1]))

    return np.array(observations), np.array(targets)

def predict(training_data: Tuple[np.array, np.array], testing_data: Tuple[np.array, np.array]) -> Any:
    X, Y = training_data
    X_test, Y_test = testing_data
    linear_regression = LinearRegression().fit(X, Y)
    Y_pred = linear_regression.predict(X_test)
    print(f'Mean squared error: {mean_squared_error(Y_test, Y_pred)}')
    print(f'Coefficient of determination: {r2_score(Y_test, Y_pred)}')
    return linear_regression

if __name__ == '__main__':
    random_qber_training_data = get_all_observations_and_targets(RANDOM_QBER_DATA_PATH)
    random_qber_testing_data = get_all_observations_and_targets(RANDOM_QBER_TEST_DATA_PATH)

    bursty_qber_training_data = get_all_observations_and_targets(BURSTY_QBER_DATA_PATH)
    bursty_qber_testing_data = get_all_observations_and_targets(BURSTY_QBER_TEST_DATA_PATH)

    random_qber_linear_regression = predict(random_qber_training_data, random_qber_testing_data)
    bursty_qber_linear_regression = predict(bursty_qber_training_data, bursty_qber_testing_data)

