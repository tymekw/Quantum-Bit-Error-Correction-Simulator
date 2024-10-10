from typing import Union, Optional

import numpy as np


class TPM:
    def __init__(
            self,
            inputs_per_hidden_later: int,
            hidden_layer_nodes: int,
            weights_range: int,
            input_layer_weights: np.array
    ):
        self._hidden_layer_nodes: int = hidden_layer_nodes
        self._input_nodes_per_hidden_layer: int = inputs_per_hidden_later
        self._weights_range: int = weights_range
        self._hidden_layer_weights: np.array = input_layer_weights
        self._input_nodes: np.array = None
        self._input_layer_weights: np.array = None
        self._result: Optional[int] = None

    def get_updated_result_and_hidden_layer_weights(self) -> Union[int, np.array]:
        updated_hidden_layer_weights = np.array(
            [
                -1 if x == 0 else x
                for x in np.sign(np.sum(np.multiply(self._input_nodes, self._hidden_layer_weights), axis=1))
            ]
        )
        updated_result = np.prod(updated_hidden_layer_weights)
        return updated_result, updated_hidden_layer_weights

    def update_input_nodes(self, input_nodes: np.array) -> None:
        self._input_nodes = input_nodes

    def update_hidden_layer_weights(self, hidden_layer_weights: np.array) -> None:
        self._hidden_layer_weights = hidden_layer_weights

    def update_result(self, result: int) -> None:
        self._result = result

    def update_weights(self) -> None:
        def get_theta(sigma_k: int) -> int:
            return 0 if sigma_k != self._result else 1

        new_weights = np.empty([self._hidden_layer_nodes, self._input_nodes_per_hidden_layer])
        for (k, n), _ in np.ndenumerate(self._input_nodes):
            z = (
                    self._input_layer_weights[k, n] +
                    self._input_nodes[k, n] * self._hidden_layer_weights[k] * get_theta(self._hidden_layer_weights[k])
            )
            if z <= -self._weights_range:
                new_weights[k, n] = -self._weights_range
            elif z >= self._weights_range:
                new_weights[k, n] = self._weights_range
            else:
                new_weights[k, n] = int(z)

        self._input_layer_weights = new_weights

