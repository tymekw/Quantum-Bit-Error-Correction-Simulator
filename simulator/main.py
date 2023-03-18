import argparse
import csv
import itertools
import time

import numpy as np

from neural_crypto.TPM.TPM import TPM
from neural_crypto.simulator.common import generate_random_input, generate_weights

parser = argparse.ArgumentParser(description="Simulate TPM to correct errors.")
parser.add_argument(
    "-l",
    "--weights_range",
    type=int,
    nargs="+",
    help="list of Ls (range of weights {-L,L}) to generate data, separated by SPACE",
)
parser.add_argument(
    "-n",
    "--number_of_inputs_per_neuron",
    type=int,
    nargs="+",
    help="Ns (numbers of inputs to a single neuron) to generate data, [from to by] separated by SPACE",
)

parser.add_argument(
    "-k",
    "--number_of_neurons_in_hidden_layer",
    type=int,
    nargs="+",
    help="Ks (numbers of neurons in hidden layer) to generate data, [from to by] separated by SPACE",
)

parser.add_argument(
    "-b",
    "--QBER",
    type=int,
    nargs="+",
    help="set list of QBERs to generate data about, separated by SPACE",
)

parser.add_argument(
    "-f",
    "--filename",
    type=str,
    help="name of file to save data to [test iterations.csv]",
)

args = parser.parse_args()

if args.weights_range:
    L = [int(i) for i in args.weights_range]
if args.QBER:
    QBER = [int(i) for i in args.QBER]
if args.number_of_inputs_per_neuron:
    N = [int(i) for i in range(args.number_of_inputs_per_neuron[0], args.number_of_inputs_per_neuron[1],
                               args.number_of_inputs_per_neuron[2])]
if args.number_of_neurons_in_hidden_layer:
    K = [int(i) for i in range(args.number_of_neurons_in_hidden_layer[0], args.number_of_neurons_in_hidden_layer[1],
                               args.number_of_neurons_in_hidden_layer[2])]

if args.filename:
    if args.filename.endswith(".csv"):
        filename = args.filename
else:
    filename = "test_iterations.csv"
    print("using default filename: test_iterations.csv")

data_rows = ["L", "N", "K", "QBER", "ERRORS", "QBER_TYPE", "REP", "TAU_MISSES", "TIME", "REPETITIONS"]
with open(filename, "a+", newline='') as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(data_rows)

REPS_FOR_STATS = 2
BER_TYPES = ("random", "bursty")

for l, n, k, ber, ber_type, rep in itertools.product(L, N, K, QBER, BER_TYPES, range(REPS_FOR_STATS)):
    initial_weights_alice, initial_weights_bob, different_weights = generate_weights(
        ber, ber_type, k, n, l
    )
    alice = TPM(n, k, l, initial_weights_alice)
    bob = TPM(n, k, l, initial_weights_bob)
    print("#" * 10)
    print("OK!")
    runs = 0
    tau_not_hit = 0
    start_time = time.time()
    while not np.array_equal(alice.W, bob.W):
        runs += 1
        X = generate_random_input(k, n)
        alice.set_X(X)
        bob.set_X(X)
        a_tau, a_sigma = alice.calculate_TPM_results()
        b_tau, b_sigma = bob.calculate_TPM_results()
        while a_tau != b_tau:
            tau_not_hit += 1
            X = generate_random_input(k, n)
            alice.set_X(X)
            bob.set_X(X)
            a_tau, a_sigma = alice.calculate_TPM_results()
            b_tau, b_sigma = bob.calculate_TPM_results()
        alice.set_tau(a_tau)
        alice.set_sigma(a_sigma)
        bob.set_tau(a_tau)
        bob.set_sigma(a_sigma)
        alice.update_weights()
        bob.update_weights()
    execution_time = time.time() - start_time
    data_row = [l, n, k, different_weights, ber, ber_type, rep, tau_not_hit, execution_time, runs]

    with open(filename, "a+", newline='') as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(data_row)
