from argparse import Namespace
from pathlib import Path
from unittest.mock import ANY, sentinel

import pytest

from simulator.args_parser import (
    translate_args_to_simulator_parameters,
    SimulatorParameters,
    Range,
    ArgumentRangeException,
)


@pytest.fixture
def base_args():
    def _get_args(
        number_of_inputs_per_neuron,
        number_of_neurons_in_hidden_layer,
    ):
        return Namespace(
            weights_range=[sentinel.w_range_1, sentinel.w_range_2],
            QBER=[sentinel.qber_1, sentinel.qber_2, sentinel.qber_3],
            number_of_inputs_per_neuron=number_of_inputs_per_neuron,
            number_of_neurons_in_hidden_layer=number_of_neurons_in_hidden_layer,
            file_path="/path/to/file",
            eve=False,
        )

    return _get_args


def test_translate_args_to_simulator_parameters(base_args):
    correct_args = base_args([10, 100, 1], [20, 30, 1])
    parameters = translate_args_to_simulator_parameters(correct_args)

    assert isinstance(parameters, SimulatorParameters)
    assert parameters.weights_range == correct_args.weights_range
    assert parameters.qber_values == correct_args.QBER
    assert parameters.range_of_inputs_per_neuron == Range(10, 100, 1)
    assert parameters.range_of_neurons_in_hidden_layer == Range(20, 30, 1)
    assert parameters.file_path == Path(correct_args.file_path)
    assert parameters.eve == correct_args.eve


@pytest.mark.parametrize(
    "number_of_inputs_per_neuron, number_of_neurons_in_hidden_layer",
    (([ANY, ANY], [ANY, ANY, ANY]), ([ANY, ANY, ANY], [ANY, ANY])),
)
def test_translate_args_to_simulator_parameters_raises(
    number_of_inputs_per_neuron, number_of_neurons_in_hidden_layer, base_args
):
    incorrect_args = base_args(
        number_of_inputs_per_neuron, number_of_neurons_in_hidden_layer
    )

    with pytest.raises(ArgumentRangeException):
        translate_args_to_simulator_parameters(incorrect_args)
