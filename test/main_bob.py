import math

import bob_client
import time

bob = bob_client.BobClient()


def get_possible_N_K(bits_len):
    factors = get_factors_list(bits_len)
    return get_best_pair(factors)

def get_factors_list(number):
    factors =[]
    for i in range(1, number+1):
        if number % i == 0:
            factors.append((i, int(number/i)))
    return factors

def get_best_pair(factors):
    best_pair = None
    tmp = math.inf
    for factor_pair in factors:
        dif = max(factor_pair) - min(factor_pair)
        if tmp > dif:
            best_pair = factor_pair
            tmp = dif

    return best_pair

def check_N_K(N, K, bits_len):
    return N*K < bits_len


print("alice bind")
time.sleep(2)
print("bob bind")
bob.bind()
time.sleep(2)
print("alice create machine")
time.sleep(2)
print("alice send machine")
time.sleep(2)
print("bob receive machine")
bob.receive_machine_config()
time.sleep(2)
print("Create bits")
bob.create_random_bits()
time.sleep(2)
print("bob create machine")
bob.create_machine()
print("K: {}, N : {}".format(bob.K, bob.N))
print("alice run")
time.sleep(2)
print("bob run")
bob.run_TPM_machine()