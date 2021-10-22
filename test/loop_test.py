import numpy as np
from numpy import random
import alice_server, bob_client
import matplotlib.pyplot as plt
import statistics

Ls = [2, 3, 4, 5]
BERs = [1, 2, 3, 4, 5]
b_lens = [128, 256]


b_len = 300
L = 2
BER = 3
results = []
for i in range(0, 500):
    # print(i)
    alice = alice_server.AliceServer()
    bob = bob_client.BobClient()

    alice.set_bits_length(b_len)
    alice.set_L(L)
    alice.set_seed("seed")
    alice.generate_bits()

    alice.create_machine()
    bob.get_config(alice.N, alice.K, alice.L, alice.seed, alice.bits_length)
    bob.bits.BER = BER
    bob.create_random_bits()
    bob.create_machine()

    s = 0
    while not np.array_equal(alice.W, bob.W_bob):
        X = np.random.choice([-1,1], size=(alice.K, alice.N))
        alice.alice.calculate_tau(X)
        bob.bob.calculate_tau(X)
        w_l = 0
        while alice.alice.tau != bob.bob.tau:
            X = np.random.choice([-1,1], size=(alice.K, alice.N))
            alice.alice.calculate_tau(X)
            bob.bob.calculate_tau(X)
            w_l += 1
            if w_l > 10:
                break

        alice.W = alice.alice.update_weights(X)
        bob.W_bob = bob.bob.update_weights(X)

        s += 1
        if w_l > 10:
            s = 0
            break
        # print(s)
    results.append(s)



results = [i for i in results if i != 0]
print(len(results))
print(sum(results)/len(results))
print(min(results))
print(max(results))
print(statistics.median(results))

fig, ax = plt.subplots()
plt.hist(x=results, bins='auto')
plt.title("Number of required synchronizations for TPM with parameters: \n N={}, K={}, L={}".format(alice.N, alice.K, L))
plt.xlabel("Number of TPM synchronizations")
plt.yticks([])
plt.show()

# a = np.hstack((results.normal(size=1000),
#                rng.normal(loc=5, scale=2, size=1000)))