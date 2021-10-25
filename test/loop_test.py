import numpy as np
from numpy import random
import alice_server, bob_client
import csv
# 18:25
#from 216 one last, 23:55 no writing to data{}
REPETITIONS = 600
Ls = [2, 3, 4]
BERs = [1, 2, 3]
b_lens = [i for i in range(224, 448, 8)]


# fields = ["bits_len", "L", "BER", "N", "K", "results"]
# with open("new_test.csv", "a+") as f:
#     w = csv.writer(f, delimiter=';')
#     w.writerow(fields)

# data = {}
for b_len in b_lens:
    # data[str(b_len)] = {}
    for l in Ls:
        # data[str(b_len)][str(l)] = {}
        aliceTEST = alice_server.AliceServer()
        aliceTEST.set_bits_length(b_len)
        aliceTEST.set_L(l)
        aliceTEST.set_seed("seed")
        aliceTEST.generate_bits()
        N_K_list = aliceTEST.get_factors_list()

        for ber in BERs:
            # data[str(b_len)][str(l)][str(ber)] = {}
            for N, K in N_K_list:
                print("B_LEN:{}, L:{}, BER:{}, N:{}, K:{}".format(b_len, l, ber, N, K))
                results = []
                if N == 1:
                    continue
                # data[str(b_len)][str(l)][str(ber)][str(N)] = {}
                # data[str(b_len)][str(l)][str(ber)][str(N)][str(K)] = {}
                # print("NEW N:{}, K: {}, BER: {}, L: {}".format(N, K, ber, l))
                print("current bits length checked: {}".format(b_len))
                for i in range(0, REPETITIONS):
                    alice = alice_server.AliceServer()
                    bob = bob_client.BobClient()

                    alice.set_bits_length(b_len)
                    alice.set_L(l)
                    alice.set_seed("seed")
                    alice.generate_bits()
                    alice.set_N(N)
                    alice.set_K(K)
                    alice.create_machine()
                    bob.get_config(alice.N, alice.K, alice.L, alice.seed, alice.bits_length)
                    bob.bits.BER = ber
                    bob.create_random_bits()
                    bob.create_machine()

                    s = 0
                    while not np.array_equal(alice.W, bob.W_bob):
                        if s == 1000:
                            break
                        X = np.random.choice([-1, 1], size=(alice.K, alice.N))
                        alice.alice.calculate_tau(X)
                        bob.bob.calculate_tau(X)
                        w_l = 0
                        while alice.alice.tau != bob.bob.tau:
                            X = np.random.choice([-1, 1], size=(alice.K, alice.N))
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
                    results.append(s)

                results = [i for i in results if i != 0]
                results = results[0:500]
                # data[str(b_len)][str(l)][str(ber)][str(N)][str(K)] = results
                with open("new_test.csv", "a+") as f:
                    w = csv.writer(f, delimiter=';')
                    row = [str(b_len), str(l), str(ber), str(N), str(K), ",".join([str(i) for i in results])]
                    w.writerow(row)

                # data[b_len][l][ber][N][K] = [str(i) for i in results]

                # print(len(results))
                # print(sum(results)/len(results))
                # print(min(results))
                # print(max(results))
                # print(statistics.median(results))
                #
                # fig, ax = plt.subplots()
                # plt.hist(x=results, bins='auto')
                # plt.title("Number of required synchronizations for TPM with parameters: \n N={}, K={}, L={}".format(alice.N, alice.K, L))
                # plt.xlabel("Number of TPM synchronizations")
                # plt.yticks([])
                # plt.show()
#
# # a = np.hstack((results.normal(size=1000),
# #                rng.normal(loc=5, scale=2, size=1000)))

# print("done")
# print(data)
# print(yaml.dump(data, allow_unicode=True, default_flow_style=False))
