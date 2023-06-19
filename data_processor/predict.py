import csv
from typing import Tuple, Any

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.svm import SVR

from neural_crypto.data_processor.common import (
    RANDOM_QBER_DATA_PATH,
    RANDOM_QBER_TEST_DATA_PATH,
    BURSTY_QBER_DATA_PATH,
    BURSTY_QBER_TEST_DATA_PATH, RANDOM_QBER_STATS_DATA_PATH,
)


def get_all_observations_and_targets(filename: str) -> Tuple[np.array, np.array]:
    with open(filename, 'r') as data_file:
        reader = csv.reader(data_file, delimiter=';')
        next(reader, None) # skip header
        observations = []
        targets = []
        for row in reader:
            observations.append([int(i) for i in row[:-1]])
            targets.append(int(row[-1]))

    return np.array(observations), np.array(targets)

def get_max_observations_and_targets(stats_filename: str) -> Tuple[np.array, np.array]:
    with open(stats_filename, 'r') as data_file:
        reader = csv.reader(data_file, delimiter=';')
        next(reader, None) # skip header
        observations = []
        targets = []
        for row in reader:
            observations.append([int(i) for i in row[0:4]])
            targets.append(int(row[4]))

    return np.array(observations), np.array(targets)





def predict(training_data: Tuple[np.array, np.array], testing_data: Tuple[np.array, np.array]) -> Any:
    X, Y = training_data
    X_test, Y_test = testing_data
    linear_regression = LinearRegression().fit(X, Y)
    Y_pred = linear_regression.predict(X_test)
    # svr_poly = SVR(kernel="poly").fit(X, Y)
    # Y_pred = svr_poly.predict(X_test)
    print(f'Mean squared error: {mean_squared_error(Y_test, Y_pred)}')
    print(f'Coefficient of determination: {r2_score(Y_test, Y_pred)}')
    return Y_pred

def display_data(observations: np.array, targets: np.array, predicted: np.array) -> None:
    with open(RANDOM_QBER_DATA_PATH, 'r') as f:
        temp = f.read().splitlines()
        lines = [line.split(';') for line in temp][1:]
        data = [[float(i) for i in row] for row in lines]
        # L, N*K, QBER, MAX, MIN, MEAN, MEDIAN, STD_DEV, VAR
        data = [[row[0], row[1] * row[2], *row[3:]] for row in data]
        data.sort(key=lambda x: (x[0], x[2], x[1])) # sorted by L, QBER than N*K
        l_3 = list(filter(lambda x: x[0] == 3.0, data)) # only with L==3
        n_ks = [row[1] for row in l_3]
        y = [row[3] for row in l_3]
        plt.scatter(n_ks, y)
        plt.show()


        qber_8 = list(filter(lambda x: x[2] == 8.0, l_3)) # only with QBER==8
        n_ks = [row[1] for row in qber_8]
        y = [row[5] for row in qber_8]
        plt.scatter(n_ks, y)
        plt.show()

    print('OK')







if __name__ == '__main__':
    random_qber_training_data = get_all_observations_and_targets(RANDOM_QBER_DATA_PATH)
    random_qber_testing_data = get_all_observations_and_targets(RANDOM_QBER_TEST_DATA_PATH)

    # bursty_qber_training_data = get_all_observations_and_targets(BURSTY_QBER_DATA_PATH)
    # bursty_qber_testing_data = get_all_observations_and_targets(BURSTY_QBER_TEST_DATA_PATH)

    random_qber_predicted = predict(random_qber_training_data, random_qber_testing_data)
    # bursty_qber_predicted = predict(bursty_qber_training_data, bursty_qber_testing_data)
    #
    #
    # random_qber_training_data_max = get_max_observations_and_targets(RANDOM_QBER_STATS_DATA_PATH)
    # random_qber_testing_data = get_all_observations_and_targets(RANDOM_QBER_TEST_DATA_PATH)

    display_data(*random_qber_training_data, random_qber_predicted)

    # bursty_qber_training_data = get_all_observations_and_targets(BURSTY_QBER_DATA_PATH)
    # bursty_qber_testing_data = get_all_observations_and_targets(BURSTY_QBER_TEST_DATA_PATH)

    # random_qber_on_max_predicted = predict(random_qber_training_data_max, random_qber_testing_data)
    # print('OK')
    # bursty_qber_predicted = predict(bursty_qber_training_data, bursty_qber_testing_data)







