# ToDo PoC main py
import copy
from random import randint
from typing import Tuple

import numpy as np

from neural_crypto.TPM.TPM import TPM

L = (5,)
N = (200,)
K = (100,)
BER = (5,)
REPS_FOR_STATS = (1,)
ber_type = 'bursty'


def add_random_errors(coding: int, ber: int, weights: np.array) -> np.array:
    k, n = np.shape(weights)
    number_of_different_weights = int((0.01 * ber * k * n))
    for error in number_of_different_weights:
        pass
    return weights


def add_bursty_errors(coding: int, ber: int, weights: np.array) -> np.array:
    k, n = np.shape(weights)
    number_of_different_weights = int((0.01 * ber * k * n) / coding)
    starting_error = randint(0, k)
    idx = 0
    for _ in range(number_of_different_weights):
        if idx < n - 1:
            weights[starting_error][idx] = randint(-l, l)
        else:
            idx = 0
            if starting_error < k - 1:
                starting_error += 1
            else:
                starting_error -= 1
        idx += 1
    return weights


def generate_weights(ber: int, ber_type: str, k, n, l) -> Tuple[np.array, np.array]:
    weights = np.random.randint(low=-l, high=l, size=(k, n))
    weights_bob = copy.deepcopy(weights)
    if ber_type == 'bursty':
        weights_bob = add_bursty_errors(8, ber, weights_bob)

    elif ber_type == 'random':
        weights_bob = add_random_errors(8, ber, weights_bob)

    return weights, weights_bob


def generate_random_input(k, n):
    return np.random.choice([-1, 1], size=(k, n))


for l in L:
    for n in N:
        for k in K:
            for ber in BER:
                for _ in REPS_FOR_STATS:
                    # change_random_seed()

                    initial_weights_alice, initial_weights_bob = generate_weights(ber, ber_type, k, n, l)
                    alice = TPM(n, k, l, initial_weights_alice)
                    bob = TPM(n, k, l, initial_weights_bob)
                    print("#" * 10)
                    print("OK!")
                    i = 0
                    while not np.array_equal(alice.W, bob.W):
                        print('OK LETS GO!')
                        i += 1
                        X = generate_random_input(k, n)
                        alice.set_X(X)
                        bob.set_X(X)
                        a_tau, a_sigma = alice.calculate_TPM_results()
                        b_tau, b_sigma = bob.calculate_TPM_results()
                        while a_tau != b_tau:
                            print("Oh noooo...")
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
                    print("DOOOOOOOOOOOOOOOOOOOOOOOOOOOONE")
                    print(i)
