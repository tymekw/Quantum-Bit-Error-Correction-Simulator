import copy
import math
import random
from statistics import mean
from typing import Tuple

import numpy as np

CODING = 4


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
    coding: int, qber: int, weights: np.array, l: int
) -> Tuple[np.array, int]:
    """
    Adds errors to the weights to simulate QBER. Errors are in a single chunk, one after another.
    coding -> number of bits required for a single weight
    """

    k, n = np.shape(weights)
    number_of_bits = k * n * coding

    min_different_weights = int(
        (number_of_bits / coding) * qber * 0.01
    )  # coding bits wrong in each 'bad' weight

    starting_error = random.randint(0, k - 1)
    idx = 0
    for _ in range(min_different_weights):
        if idx < n - 1:
            weights[starting_error][idx] = random_number_excluded(
                l, weights[starting_error][idx]
            )
            idx += 1
        else:
            idx = 0
            if starting_error < k - 1:
                starting_error += 1
            else:
                starting_error -= 1
    return weights, min_different_weights


def generate_weights(
    ber: int, ber_type: str, k: int, n: int, l: int
) -> Tuple[np.array, np.array, int]:
    CODING = int(math.ceil(math.log2(2 * l + 1)))
    weights = np.random.randint(low=-l, high=l, size=(k, n))
    weights_bob = copy.deepcopy(weights)
    different_weights = 0
    if ber_type == "bursty":
        weights_bob, different_weights = add_bursty_errors(CODING, ber, weights_bob, l)

    elif ber_type == "random":
        weights_bob, different_weights = add_random_errors(CODING, ber, weights_bob, l)

    return weights, weights_bob, different_weights


def generate_random_input(k, n):
    return np.random.choice([-1, 1], size=(k, n))
