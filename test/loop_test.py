import numpy as np
import alice_server, bob_client

b_len = 1000
L = 2
BER = 4
results = []
for i in range(0, 1):
    alice = alice_server.AliceServer()
    bob = bob_client.BobClient()

    alice.set_bits_length(b_len)
    alice.set_L(L)
    alice.set_seed("seed")
    alice.generate_bits()

    alice.create_machine()
    print(alice.W)
    print("N: {}".format(alice.N))
    print("K: {}".format(alice.K))
    print("L: {}".format(alice.L))
    bob.get_config(alice.N, alice.K, alice.L, alice.seed, alice.bits_length)
    bob.bits.BER = BER
    bob.create_random_bits()
    # print(bob.bits.bits)
    # print(alice.bits.bits)



    bob.create_machine()
    # print("bob")
    # print(bob.W_bob)
    # print(bob.bob.W)
    #
    # print(alice.W)

    s = 0
    while not np.array_equal(alice.alice.W, bob.bob.W):
        X = np.random.randint(-1, 2, size=(alice.K, alice.N))
        alice.alice.calculate_tau(X)
        bob.bob.calculate_tau(X)
        while alice.alice.tau != bob.bob.tau:
            X = np.random.randint(-1, 2, size=(alice.K, alice.N))
            alice.alice.calculate_tau(X)
            bob.bob.calculate_tau(X)
            print("new X vector")

        alice.W = alice.alice.update_weights(X)
        bob.W_bob = bob.bob.update_weights(X)

        s += 1
        print(s)
    results.append(s)

print(sum(results)/len(results))
print(min(results))
print(max(results))

