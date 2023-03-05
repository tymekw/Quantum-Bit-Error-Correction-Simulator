# ToDo PoC main py
import copy
from typing import Tuple

import numpy as np

from neural_crypto.TPM.TPM import TPM

NUMBER_OF_BITS = (100, 200, 300)
L = (3,5)
N = (5, 10, 15)
K = (5, 10, 15)
BER = (1,2,3,4,5)
REPS_FOR_STATS = (1,)
ber_type = 'random'

def generate_weigths(ber: int, ber_type: str, k, n, l) -> Tuple[np.array, np.array]:
     weights = np.random.randint(low=-l, high=l, size = (k, n))
     weights_bob = copy.deepcopy(weights)
     if weights_bob[1,1] != 1:
         weights_bob[1, 1] = 1
     else:
         weights_bob[1, 1] = 2

     return weights, weights_bob

def generate_random_input(k, n):
    return np.random.choice([-1, 1], size=(k, n))

for n_of_bits in NUMBER_OF_BITS:
    for l in L:
        for n in N:
            for k in K:
                for ber in BER:
                    for _ in REPS_FOR_STATS:
                        # change_random_seed()
                        initial_weights_alice, initial_weights_bob = generate_weigths(ber, ber_type, k, n, l)
                        alice = TPM(n,k,l, initial_weights_alice)
                        bob = TPM(n,k,l, initial_weights_bob)
                        print("#"*10)
                        print("OK DONE!")
                        while not np.array_equal(alice.W,bob.W):
                            print('OK LETS GO!')
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
