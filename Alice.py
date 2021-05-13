import TPM
import numpy as np

N = 10
K = 10
L = 10

W = np.random.randint(-L, L + 1, size=(K, N))
W_bob = np.random.randint(-L, L + 1, size=(K, N))

alice = TPM.Tpm(N, K, L, W)
bob = TPM.Tpm(N, K, L, W_bob)

s = 0
while not np.array_equal(alice.W, bob.W):
    X = np.random.randint(-L, L + 1, size=(K, N))
    alice.calculate_tau(X)
    bob.calculate_tau(X)
    while alice.tau != bob.tau:
        X = np.random.randint(-L, L + 1, size=(K, N))
        alice.calculate_tau(X)
        bob.calculate_tau(X)
        print("new X vector")

    alice.update_weights(X)
    bob.update_weights(X)

    s += 1
    print(s)
