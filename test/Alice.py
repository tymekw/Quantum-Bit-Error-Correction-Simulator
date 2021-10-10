import math
import TPM
import numpy as np
import bits

L = 2

bob_b = bits.Bits(L)
alice_b = bits.Bits(L)

bob_b.generate_bits(100, 300)
alice_b.generate_bits(100, 300)
bob_b.type = 'block'
bob_b.BER = 30
bob_b.create_BER()


def get_possible_N_K(bits_len):
    factors = get_factors_list(bits_len)
    # return get_best_pair(factors)
    return factors

def get_factors_list(number):
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append((i, int(number / i)))
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
    return N * K < bits_len


# best_pair = get_possible_N_K(len(bits_alice))
# print(best_pair)

#
# N = 20
# K = 15
# print(check_N_K(N, K, len(bits_alice)))

# fink K and L
bits_len = len(alice_b.bits_to_w())
print(bits_len)
print(get_possible_N_K(bits_len))

K = 2
N = 43
W_bob = bob_b.bits_to_arr(K, N)
W = alice_b.bits_to_arr(K, N)

alice = TPM.Tpm(N, K, L, W)
bob = TPM.Tpm(N, K, L, W_bob)

s = 0
while not np.array_equal(alice.W, bob.W):
    X = np.random.randint(-1, 2, size=(K, N))
    alice.calculate_tau(X)
    bob.calculate_tau(X)
    while alice.tau != bob.tau:
        X = np.random.randint(-1, 2, size=(K, N))
        alice.calculate_tau(X)
        bob.calculate_tau(X)
        print("new X vector")

    alice.update_weights(X)
    bob.update_weights(X)

    s += 1
    print(s)

# b = bits.Bits(2)
# print(len(b.arr_to_bits(alice.W, alice_b.max_val)))
# print(len(b.arr_to_bits(bob.W, bob_b.max_val)))

new_bits_bob = bob_b.arr_to_bits(bob.W, 256)
new_bits_alice = alice_b.arr_to_bits(alice.W, 256)
# print(bob_b.bits)
# print(alice_b.bits)
# print(len())