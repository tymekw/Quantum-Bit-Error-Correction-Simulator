import numpy as np
import hashlib


def calculate_theta(sigma_k, tau):
    return 0 if sigma_k != tau else 1


def sha256(numpy_array):
    return hashlib.sha256(numpy_array.tobytes()).digest()


class Tpm:
    def __init__(self, n, k, l, w):
        self.sigma = None
        self.tau = None
        self.N = n
        self.K = k
        self.L = l
        self.W = w

    def calculate_tau(self, X):
        sigma = np.sign(np.sum(X * self.W, axis=1))
        sigma = np.array([-1 if x == 0 else x for x in sigma])
        tau = np.prod(sigma)
        self.tau = tau
        self.sigma = sigma

    def update_weights(self, X):
        self.calculate_tau(X)
        w_new = np.empty([self.K, self.N])
        for (k, n), _ in np.ndenumerate(X):
            z = self.W[k, n] + X[k, n] * self.sigma[k] * calculate_theta(self.sigma[k], self.tau)
            if z <= -self.L:
                w_new[k, n] = int(-self.L)
            elif z >= self.L:
                w_new[k, n] = int(self.L)
            else:
                w_new[k, n] = int(z)
        self.W = w_new
        return w_new
