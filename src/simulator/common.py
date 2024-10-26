import copy
import math
import random
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from statistics import mean
from typing import Tuple
import numpy.typing as npt
import numpy as np

from tree_parity_machine.tree_parity_machine import TMPBaseParameters

CODING = 4
REPS_FOR_STATS = 4


class BerTypes(Enum):
    RANDOM = "random"
    BURSTY = "bursty"


@dataclass
class SimulatorParameters:
    weights_range: list[int]
    range_of_inputs_per_neuron: range
    qber_values: list[int]
    range_of_neurons_in_hidden_layer: range
    file_path: Path
    eve: int
    repetitions: range = range(REPS_FOR_STATS)
    ber_types: tuple[str] = tuple(BerTypes)

    def get_iteration_params(self):
        return (
            self.weights_range,
            self.range_of_inputs_per_neuron,
            self.range_of_neurons_in_hidden_layer,
            self.qber_values,
            self.ber_types,
            self.repetitions,
        )


class SimulatorException(BaseException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


def random_number_excluded(range_limit: int, excluded: int) -> int:
    return random.choice(
        list(set([_ for _ in range(-range_limit, range_limit)]) - {excluded})
    )


def add_random_errors(
    coding: int, qber: int, weights: np.array, l: int
) -> Tuple[np.array, int]:
    """
    Adds randomly distributed errors to the weights to simulate QBER.
    coding -> number of bits required for a single weight
    """
    k, n = np.shape(weights)

    number_of_bits = k * n * coding
    max_different_weights = int(
        number_of_bits * qber * 0.01
    )  # 1 bit wrong in each 'bad' weight

    min_different_weights = int(
        (number_of_bits / coding) * qber * 0.01
    )  # coding bits wrong in each 'bad' weight

    number_of_different_weights = int(
        mean((max_different_weights, min_different_weights))
    )
    temp = weights.flatten()

    for idx in random.sample(range(k * n), number_of_different_weights):
        temp[idx] = random_number_excluded(l, temp[idx])

    return temp.reshape(k, n), number_of_different_weights


def add_bursty_errors(
    coding: int, qber: int, weights: np.array, weights_range_limit: int
) -> Tuple[np.array, int]:
    """
    Adds errors to the weights to simulate QBER. Errors are in a single chunk, one after another.
    coding -> number of bits required for a single weight
    """

    number_of_hidden_layer_nodes, number_of_input_nodes_per_hidden = np.shape(weights)
    number_of_bits = (
        number_of_hidden_layer_nodes * number_of_input_nodes_per_hidden * coding
    )

    min_different_weights = int(
        (number_of_bits / coding) * qber * 0.01
    )  # coding bits wrong in each 'bad' weight

    starting_error = random.randint(0, number_of_hidden_layer_nodes - 1)
    idx = 0
    for _ in range(min_different_weights):
        if idx < number_of_input_nodes_per_hidden - 1:
            weights[starting_error][idx] = random_number_excluded(
                weights_range_limit, weights[starting_error][idx]
            )
            idx += 1
        else:
            idx = 0
            if starting_error < number_of_hidden_layer_nodes - 1:
                starting_error += 1
            else:
                starting_error -= 1
    return weights, min_different_weights


def generate_single_tmp_weights(tmp_parameters: TMPBaseParameters):
    return np.random.randint(
        low=-tmp_parameters.weights_value_limit,
        high=tmp_parameters.weights_value_limit,
        size=(
            tmp_parameters.number_of_neurons_in_hidden_layer,
            tmp_parameters.number_of_inputs_per_neuron,
        ),
    )


def get_weights_with_error(
    hidden_layer_weights: npt.NDArray,
    weights_value_limit: int,
    ber: int,
    ber_type: BerTypes,
) -> tuple[npt.NDArray, int]:
    coding = int(math.ceil(math.log2(2 * weights_value_limit + 1)))
    return_weights = copy.deepcopy(hidden_layer_weights)
    number_of_different_weights = 0
    if ber_type is BerTypes.BURSTY:
        return_weights, number_of_different_weights = add_bursty_errors(
            coding, ber, return_weights, weights_value_limit
        )
    elif ber_type is BerTypes.RANDOM:
        return_weights, number_of_different_weights = add_random_errors(
            coding, ber, return_weights, weights_value_limit
        )
    return return_weights, number_of_different_weights


def generate_random_input(k, n):
    return np.random.choice([-1, 1], size=(k, n))
