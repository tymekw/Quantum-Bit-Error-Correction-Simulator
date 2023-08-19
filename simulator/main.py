import argparse
import csv
import itertools
import math
import time

import numpy as np

from TPM.TPM import TPM
from simulator.common import generate_random_input, generate_weights

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
    "-e",
    "--eve",
    type=int,
    help="number of Eve's machines",
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
    filename = "../results/partial/test_eve.csv"
    print("using default filename: test_iterations_coding_L5.csv")

if args.eve:
    EVE = args.eve
    data_rows = ["L", "N", "K", "QBER", "ERRORS", "QBER_TYPE", "REP", "TAU_MISSES", "TIME", "REPETITIONS", "EVE_SUCCESS", "EVE_REQUIRED"]
else:
    EVE = 0
    data_rows = ["L", "N", "K", "QBER", "ERRORS", "QBER_TYPE", "REP", "TAU_MISSES", "TIME", "REPETITIONS"]


with open(filename, "a+", newline='') as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(data_rows)

REPS_FOR_STATS = 6
BER_TYPES = ("random", "bursty")
if not EVE:
    for l, n, k, ber, ber_type, rep in itertools.product(L, N, K, QBER, BER_TYPES, range(REPS_FOR_STATS)):
        initial_weights_alice, initial_weights_bob, different_weights = generate_weights(
            ber, ber_type, k, n, l
        )
        print(f'l:{l}, n:{n}, k:{k}, ber:{ber}, ber_type:{ber_type}, rep:{rep}')
        alice = TPM(n, k, l, initial_weights_alice)
        bob = TPM(n, k, l, initial_weights_bob)
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
        data_row = [l, n, k, ber, different_weights, ber_type, rep, tau_not_hit, execution_time, runs]

        with open(filename, "a+", newline='') as f:
            w = csv.writer(f, delimiter=";")
            w.writerow(data_row)
else:
    for l, n, k, ber, ber_type, rep in itertools.product(L, N, K, QBER, BER_TYPES, range(REPS_FOR_STATS)):
        initial_weights_alice, initial_weights_bob, different_weights = generate_weights(
            ber, ber_type, k, n, l
        )
        eves_weights = [generate_weights(ber, ber_type, k, n, l)[0] for _ in range(EVE)]

        print(f'l:{l}, n:{n}, k:{k}, ber:{ber}, ber_type:{ber_type}, rep:{rep}')
        alice = TPM(n, k, l, initial_weights_alice)
        bob = TPM(n, k, l, initial_weights_bob)
        eves = [TPM(n, k, l, eves_weights[i]) for i in range(EVE)]
        runs_required = math.inf
        runs = 0
        eve_runs = 0
        tau_not_hit = 0
        start_time = time.time()
        eve_updated = 0
        success_eve = 0
        while not any(np.array_equal(alice.W, eve.W) for eve in eves):
            if np.array_equal(alice.W, bob.W):
                runs_required = min(runs, runs_required)
            else:
                runs += 1

            eve_runs += 1
            X = generate_random_input(k, n)
            alice.set_X(X)
            bob.set_X(X)
            a_tau, a_sigma = alice.calculate_TPM_results()
            b_tau, b_sigma = bob.calculate_TPM_results()
            [eve.set_X(X) for eve in eves]
            eves_taus = [eve.calculate_TPM_results()[0] for eve in eves]
            eves_sigmas = [eve.calculate_TPM_results()[1] for eve in eves]

            while a_tau != b_tau:
                tau_not_hit += 1
                X = generate_random_input(k, n)
                alice.set_X(X)
                bob.set_X(X)
                [eve.set_X(X) for eve in eves]
                a_tau, a_sigma = alice.calculate_TPM_results()
                b_tau, b_sigma = bob.calculate_TPM_results()
                eves_taus = [eve.calculate_TPM_results()[0] for eve in eves]
                eves_sigmas = [eve.calculate_TPM_results()[1] for eve in eves]

            for eve_idx in range(EVE):
                if eves_taus[eve_idx] == a_tau:
                    eves[eve_idx].set_tau(a_tau)
                    eves[eve_idx].set_sigma(a_sigma)
                    eves[eve_idx].update_weights()
                    eve_updated += 1

            alice.set_tau(a_tau)
            alice.set_sigma(a_sigma)
            bob.set_tau(a_tau)
            bob.set_sigma(a_sigma)
            alice.update_weights()
            bob.update_weights()



        execution_time = time.time() - start_time
        for eve_idx in range(EVE):
            if np.array_equal(eves[eve_idx].W, bob.W):
                success_eve += 1
        data_row = [l, n, k, ber, different_weights, ber_type, rep, tau_not_hit, execution_time, runs_required, success_eve, eve_runs]
        print("#"*100)
        print(f'Eve sucessfull: {success_eve}')
        print(f'Eve runs: {eve_runs}')
        print(f'Alcie Bob runs: {runs_required}')

        with open(filename, "a+", newline='') as f:
            w = csv.writer(f, delimiter=";")
            w.writerow(data_row)