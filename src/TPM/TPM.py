import numpy as np


class TPM:
    def __init__(
        self,
        inputs_per_hidden_layer: int,
        hidden_layer_nodes: int,
        weights_range: int,
        initial_weights: np.array,
    ) -> None:
        self._number_of_inputs_per_hidden_layer: int = inputs_per_hidden_layer
        self._number_of_hidden_layer_nodes: int = hidden_layer_nodes
        self._weights_range_value: int = weights_range
        self.hidden_layer_weights: np.array = initial_weights
        self.result_weights: np.array | None = None
        self.result: int | None = None
        self.input_nodes: np.array | None = None

    def calculate_TPM_results(self) -> int | np.array:
        sigma = np.array(
            [
                -1 if x == 0 else x
                for x in np.sign(
                    np.sum(
                        np.multiply(self.input_nodes, self.hidden_layer_weights), axis=1
                    )
                )
            ]
        )
        tau = np.prod(sigma)
        return tau, sigma

    def update_weights(self) -> np.array:
        def get_theta(sigma_k: int) -> int:
            return 0 if sigma_k != self.result else 1

        new_weights = np.empty(
            [
                self._number_of_hidden_layer_nodes,
                self._number_of_inputs_per_hidden_layer,
            ]
        )
        for (k, n), _ in np.ndenumerate(self.input_nodes):
            z = self.hidden_layer_weights[k, n] + self.input_nodes[
                k, n
            ] * self.result_weights[k] * get_theta(self.result_weights[k])
            if z <= -self._weights_range_value:
                new_weights[k, n] = -self._weights_range_value
            elif z >= self._weights_range_value:
                new_weights[k, n] = self._weights_range_value
            else:
                new_weights[k, n] = int(z)

        self.hidden_layer_weights = new_weights

        return new_weights
