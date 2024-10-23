from argparse import Namespace
from pathlib import Path


import pytest

from simulator.args_parser import (
    translate_args_to_simulator_parameters,
    SimulatorParameters,
    Range,
)


@pytest.fixture
def base_args():
    return Namespace(
        weights_range=[-10, 10],
        QBER=[0.01, 0.1],
        number_of_inputs_per_neuron=[10, 100, 1],
        number_of_neurons_in_hidden_layer=[20, 30, 1],
        file_path="/path/to/file",
        eve=False,
    )


def test_translate_args_to_simulator_parameters(base_args):

    parameters = translate_args_to_simulator_parameters(base_args)

    assert isinstance(parameters, SimulatorParameters)
    assert parameters.weights_range == base_args.weights_range
    assert parameters.qber_values == base_args.QBER
    assert parameters.range_of_inputs_per_neuron == Range(10, 100, 1)
    assert parameters.range_of_neurons_in_hidden_layer == Range(20, 30, 1)
    assert parameters.file_path == Path(base_args.file_path)
    assert parameters.eve == base_args.eve
