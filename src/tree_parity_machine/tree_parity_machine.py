import numpy as np
import numpy.typing as npt
from dataclasses import dataclass

from numpy import signedinteger


@dataclass
class TMPBaseParameters:
    number_of_neurons_in_hidden_layer: int  # k
    number_of_inputs_per_neuron: int  # n
    weights_value_limit: int  # l


class TPM:
    def __init__(
        self,
        tmp_parameters: TMPBaseParameters,
        initial_weights: npt.NDArray,
    ) -> None:
        self.hidden_layer_weights: npt.NDArray = initial_weights
        self._number_of_inputs_per_hidden_layer: int = (
            tmp_parameters.number_of_inputs_per_neuron
        )
        self._number_of_hidden_layer_nodes: int = (
            tmp_parameters.number_of_neurons_in_hidden_layer
        )
        self._weights_range_value: int = tmp_parameters.weights_value_limit
        self._result_weights: npt.NDArray | None = None
        self._result: signedinteger | None = None
        self._input_nodes: npt.NDArray | None = None

    def set_input_nodes(self, input_nodes: npt.NDArray) -> None:
        self._input_nodes = input_nodes

    def update_result_node(
        self, result: signedinteger, result_weights: npt.NDArray
    ) -> None:
        self._result_weights = result_weights
        self._result = result

    def calculate_TPM_results(self) -> tuple[signedinteger, npt.NDArray]:
        result_weights = np.array(
            [
                -1 if x == 0 else x
                for x in np.sign(
                    np.sum(
                        np.multiply(self._input_nodes, self.hidden_layer_weights),
                        axis=1,
                    )
                )
            ]
        )
        tau = np.prod(result_weights)
        return tau, result_weights

    def update_weights(self) -> None:
        def get_theta(hidden_node_result: int) -> int:
            return 0 if hidden_node_result != self._result else 1

        new_weights = np.empty(
            [
                self._number_of_hidden_layer_nodes,
                self._number_of_inputs_per_hidden_layer,
            ]
        )
        for (hidden_node_idx, input_node_idx), _ in np.ndenumerate(self._input_nodes):
            z = self.hidden_layer_weights[
                hidden_node_idx, input_node_idx
            ] + self._input_nodes[
                hidden_node_idx, input_node_idx
            ] * self._result_weights[hidden_node_idx] * get_theta(
                self._result_weights[hidden_node_idx]
            )
            if z <= -self._weights_range_value:
                new_weights[
                    hidden_node_idx, input_node_idx
                ] = -self._weights_range_value
            elif z >= self._weights_range_value:
                new_weights[hidden_node_idx, input_node_idx] = self._weights_range_value
            else:
                new_weights[hidden_node_idx, input_node_idx] = int(z)

        self.hidden_layer_weights = new_weights
