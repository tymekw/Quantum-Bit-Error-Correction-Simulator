import TPM
import numpy as np

N = 8
K = 6
L = 2

W = np.random.randint(-L, L+1, size=(K,N))
W_bob = np.random.randint(-L, L+1, size=(K,N))

alice = TPM.Tpm(N, K, L, W)
bob = TPM.Tpm(N, K, L, W_bob)

X = np.random.randint(-L, L + 1, size=(K, N))
alice.calculate_tau(X)
bob.calculate_tau(X)

while alice.tau != bob.tau:
    X = np.random.randint(-L, L + 1, size=(K, N))
    X_bob = np.random.randint(-L, L + 1, size=(K, N))
    alice.calculate_tau(X)
    bob.calculate_tau(X)
    print("new X vector")

s= 0
while not np.array_equal(alice.W, bob.W):
    alice.update_weights(X)
    bob.update_weights(X)

    X = np.random.randint(-L, L + 1, size=(K, N))
    alice.calculate_tau(X)
    bob.calculate_tau(X)
    while alice.tau != bob.tau:
        X = np.random.randint(-L, L + 1, size=(K, N))
        alice.calculate_tau(X)
        bob.calculate_tau(X)
        print("new X vector")


    s+=1
    print(s)
