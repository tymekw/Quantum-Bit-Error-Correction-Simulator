import math
import random

import TPM
import numpy as np
import copy
# N = 6
# K = 8
# L = 2
# L = int(input("L: "))
L = 2
max_val = 2*L+1 + L//2
s = len(bin(max_val))-2

BER = 0.03


random.seed(10)
b_bob = random.getrandbits(1000)
b_bob = bin(b_bob)
b_bob = b_bob[2:]

b_bob = [i for i in b_bob]

for _ in range(int(len(b_bob)*BER)):
    if b_bob[random.randint(0,len(b_bob)-1)] == "1":
        b_bob[random.randint(0, len(b_bob) - 1)] = "0"
    else:
        b_bob[random.randint(0, len(b_bob) - 1)] = "1"


b_bob = "".join(b_bob)

bits_bob = [b_bob[i:i + s] for i in range(0, len(b_bob), s)]


random.seed(10)
b_alice = random.getrandbits(1000)
b_alice = bin(b_alice)[2:]
# b = bin(b)[2:]
bits_alice = [b_alice[i:i + s] for i in range(0, len(b_alice), s)]






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



best_pair = get_possible_N_K(len(bits_alice))
print(best_pair)


N = 20
K = 15
print(check_N_K(N, K, len(bits_alice)))







nums_alice = [int("0b" + str(bit), 2)-max_val//2 for bit in bits_alice]
print(nums_alice)
nums_bob = [int("0b" + str(bit), 2)-3 for bit in bits_bob]
print(nums_bob)
nums_alice = nums_alice[:N*K]
nums_bob = nums_bob[:N*K]

arr = np.array(nums_alice)
arr = np.reshape(arr, (K, N))
arr_bob = np.array(nums_bob)
arr_bob = np.reshape(arr_bob, (K, N))
# arr = np.squeeze(arr)
# print(arr)
# print(int("0b" + str(bits_b), 2))
# #

# W = np.random.randint(-L*10, L*10 + 1, size=(K, N))
# W_bob = np.random.randint(-L*10, L*10 + 1, size=(K, N))
W = arr
W_bob = arr_bob

alice = TPM.Tpm(N, K, L, W)
bob = TPM.Tpm(N, K, L, W_bob)

s = 0
while not np.array_equal(alice.W, bob.W):
    X = np.random.randint(-1, 2, size=(K, N))
    alice.calculate_tau(X)
    bob.calculate_tau(X)
    while alice.tau != bob.tau:
        X = np.random.randint(-1,  2, size=(K, N))
        alice.calculate_tau(X)
        bob.calculate_tau(X)
        print("new X vector")

    alice.update_weights(X)
    bob.update_weights(X)

    s += 1
    print(s)
