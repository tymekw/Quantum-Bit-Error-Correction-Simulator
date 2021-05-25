import numpy as np
import copy
import TPM

N = 8
K = 6
L = 2

same = False
while not same:
    X = np.random.randint(-L, L + 1, size=(K, N))
    X1 = X
    print(X)

    W = np.random.randint(-L, L + 1, size=(K, N))
    W1 = np.random.randint(-L, L + 1, size=(K, N))

    print(W)

    sigma = np.sign(np.sum(X * W, axis=1))
    sigma1 = np.sign(np.sum(X1 * W1, axis=1))
    sigma = np.array([-1 if x == 0 else x for x in sigma])
    sigma1 = np.array([-1 if x == 0 else x for x in sigma1])
    print(sigma)

    tau = np.prod(sigma)
    tau1 = np.prod(sigma1)
    print(tau)
    print(tau1)
    if tau == tau1:
        same = True


def theta(sigma, tau):
    return 0 if sigma != tau else 1


# print(X)
# print(X[1,1])
# print(W)


def update_weights(W, X, sigma, tau):
    w_new = np.empty([K, N])
    for (k, n), _ in np.ndenumerate(X):
        z = W[k, n] + X[k, n] * sigma[k] * theta(sigma[k], tau)
        if z <= -L:
            w_new[k, n] = int(-L)
        elif z >= L:
            w_new[k, n] = int(L)
        else:
            w_new[k, n] = int(z)
    return w_new


# print(w_new)

tmp = TPM.sha256(W)
tmp1 = TPM.sha256(W1)
s = 0
while tmp != tmp1:
    print(s)
    W = update_weights(W, X, sigma, tau)
    W1 = update_weights(W1, X1, sigma1, tau1)

    X = np.random.randint(-L, L + 1, size=(K, N))
    X1 = copy.copy(X)
    sigma = np.sign(np.sum(X * W, axis=1))
    sigma1 = np.sign(np.sum(X1 * W1, axis=1))
    sigma = np.array([-1 if x == 0 else x for x in sigma])
    sigma1 = np.array([-1 if x == 0 else x for x in sigma1])
    # print(sigma)

    tau = np.prod(sigma)
    tau1 = np.prod(sigma1)
    # print(tau)
    # print(tau1)
    while tau != tau1:
        X = np.random.randint(-L, L + 1, size=(K, N))
        X1 = X
        # print(X)

        sigma = np.sign(np.sum(X * W, axis=1))
        sigma1 = np.sign(np.sum(X1 * W1, axis=1))
        sigma = np.array([-1 if x == 0 else x for x in sigma])
        sigma1 = np.array([-1 if x == 0 else x for x in sigma1])
        # print(sigma)

        tau = np.prod(sigma)
        tau1 = np.prod(sigma1)

    tmp = TPM.sha256(W)
    tmp1 = TPM.sha256(W1)

    s += 1
