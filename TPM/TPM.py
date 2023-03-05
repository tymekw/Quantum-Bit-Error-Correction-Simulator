from typing import Union, Optional

import numpy as np


class TPM:
    def __init__(
            self,
            inputs_per_hidden_layer: int,
            hidden_layer_nodes: int,
            weights_range: int,
            initial_weights: np.array,
    ) -> None:
        self.sigma: np.array = None
        self.tau: Optional[int] = None
        self.X: np.array = None
        self.N: int = inputs_per_hidden_layer
        self.K: int = hidden_layer_nodes
        self.L: int = weights_range
        self.W: np.array = initial_weights

    def set_X(self, new_X: np.array) -> None:
        self.X = new_X

    def set_sigma(self, new_sigma: np.array) -> None:
        self.sigma = new_sigma

    def set_tau(self, new_tau: int) -> None:
        self.tau = new_tau

    def calculate_TPM_results(self) -> Union[int, np.array]:
        sigma = np.array([-1 if x == 0 else x for x in np.sign(np.sum(np.multiply(self.X, self.W), axis=1))])
        tau = np.prod(sigma)
        return tau, sigma

    def update_weights(self) -> None:
        def get_theta(sigma_k: int) -> int:
            return 0 if sigma_k != self.tau else 1

        new_weights = np.empty([self.K, self.N])
        for (k, n), _ in np.ndenumerate(self.X):
            z = self.W[k, n] + self.X[k, n] * self.sigma[k] * get_theta(self.sigma[k])
            if z <= -self.L:
                new_weights[k, n] = -self.L
            elif z >= self.L:
                new_weights[k, n] = self.L
            else:
                new_weights[k, n] = int(z)

        self.W = new_weights
        return new_weights
