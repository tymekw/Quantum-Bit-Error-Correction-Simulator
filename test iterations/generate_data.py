import argparse
import csv
import numpy as np
from numpy import random
import alice_server
import bob_client

parser = argparse.ArgumentParser()

parser.add_argument("-r", "--repetitions", type=int, help="set number of repetitions per one TPM setting, min 200")
parser.add_argument("-l", "--range", type=int, nargs='+', help="set list of Ls (range of weights {-L,L}) to generate "
                                                               "data about, separated by SPACE")
parser.add_argument("-b", "--QBER", type=int, nargs='+', help="set list of BERs to generate data about, separated by "
                                                              "SPACE")
parser.add_argument("-len", "--bits_lengths", type=int, nargs='+', help="set list of bits lengths to generate data "
                                                                        "about, separated by SPACE")
parser.add_argument("-n", "--filename", type=str, help="name of file to save data to [test iterations.csv]")
args = parser.parse_args()

if args.repetitions:
    REPETITIONS = int(args.repetitions)
    if REPETITIONS < 200:
        raise argparse.ArgumentTypeError("Minimum REPETITIONS is 200")

if args.range:
    Ls = [int(i) for i in args.range]
if args.BER:
    BERs = [int(i) for i in args.BER]
if args.repetitions:
    b_lens = [int(i) for i in args.bits_lengths]
if args.filename:
    if args.filename.endswith(".csv"):
        filename = args.filename
    else:
        filename = "test iterations.csv"
        print("using default filename: test iterations.csv")

if not REPETITIONS and Ls and BERs and b_lens:
    print("run script with proper arguments, help with --help")

fields = ["bits_len", "L", "BER", "N", "K", "results"]
with open(filename, "a+") as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(fields)

for b_len in b_lens:
    for l in Ls:
        aliceTEST = alice_server.AliceServer()
        aliceTEST.set_bits_length(b_len)
        aliceTEST.set_L(l)
        aliceTEST.set_seed("seed")
        aliceTEST.generate_bits()
        N_K_list = aliceTEST.get_factors_list()

        for ber in BERs:
            for N, K in N_K_list:
                print("B_LEN:{}, L:{}, BER:{}, N:{}, K:{}".format(b_len, l, ber, N, K))
                results = []
                if N == 1:
                    continue
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
                        alice.aliceTPM.calculate_tau(X)
                        bob.bobTPM.calculate_tau(X)
                        w_l = 0
                        while alice.aliceTPM.tau != bob.bobTPM.tau:
                            X = np.random.choice([-1, 1], size=(alice.K, alice.N))
                            alice.aliceTPM.calculate_tau(X)
                            bob.bobTPM.calculate_tau(X)
                            w_l += 1
                            if w_l > 10:
                                break

                        alice.W = alice.aliceTPM.update_weights(X)
                        bob.W_bob = bob.bobTPM.update_weights(X)

                        s += 1
                        if w_l > 10:
                            s = 0
                            break
                    results.append(s)

                results = [i for i in results if i != 0]
                results = results[0:REPETITIONS - 100]
                with open(filename, "a+") as f:
                    w = csv.writer(f, delimiter=';')
                    row = [str(b_len), str(l), str(ber), str(N), str(K), ",".join([str(i) for i in results])]
                    w.writerow(row)
