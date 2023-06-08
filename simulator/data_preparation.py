import csv

def cut_file():
    with open("test_iterations_coding1.csv", "r") as input_file:
        reader = csv.reader(input_file)

        with open("iterations_N_2_N_6_146_K_6_146_QBER_1_8_REP_5.csv", "w", newline='') as output_file:
            writer = csv.writer(output_file)
            for row in reader:
                if row[0][0] != '3':
                    writer.writerow(row)


def prepare_data():
    with open("iterations_N_2_N_6_146_K_6_146_QBER_1_8_REP_5.csv", 'r') as raw_data_file:
        reader = csv.reader(raw_data_file)

        with open("iterations_N_2_N_6_146_K_6_146_QBER_1_8_random.csv", "w", newline='') as mean_data_random:
            with open("iterations_N_2_N_6_146_K_6_146_QBER_1_8_bursty.csv", "w", newline='') as mean_data_bursty:
                writer_random = csv.writer(mean_data_random)
                writer_random.writerow(['L;N;K;QBER;REPETITIONS'])
                writer_bursty = csv.writer(mean_data_bursty)
                writer_bursty.writerow(['L;N;K;QBER;REPETITIONS'])
                for row in reader:
                    if reader.line_num > 1:
                        row  = row[0].split(';')
                        tmp = [*row[0:4], row[-1]]
                        if row[5] == 'random':
                            writer_random.writerow(tmp)
                        else:
                            writer_bursty.writerow(tmp)


import numpy as np
from sklearn.linear_model import LinearRegression

with open('iterations_N_2_N_6_146_K_6_146_QBER_1_8_random.csv', 'r') as data_file:
    X = []
    Y = []
    reader = csv.reader(data_file)
    for row in reader:
        if reader.line_num > 1:
            X.append([int(i) for i in row[:-1]])
            Y.append(int(row[-1]))
            print('OK')

X = np.array(X)
y = np.array(Y)

# X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
# # y = 1 * x_0 + 2 * x_1 + 3
# y = np.dot(X, np.array([1, 2])) + 3
reg = LinearRegression().fit(X, y)

reg.predict(np.array([[2, 18, 8, 8]]))







