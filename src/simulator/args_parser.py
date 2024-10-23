from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from pathlib import Path

DEFAULT_FILENAME = "tmp_test_result.csv"


@dataclass
class Range:
    min: int
    max: int
    step: int


@dataclass
class SimulatorParameters:
    weights_range: list[int]
    range_of_inputs_per_neuron: Range
    qber_values: list[int]
    range_of_neurons_in_hidden_layer: Range
    file_path: Path
    eve: int


def parse_arguments() -> Namespace:
    parser = ArgumentParser(description="Simulate TPM to correct errors.")
    parser.add_argument(
        "-l",
        "--weights_range",
        type=int,
        required=True,
        nargs="+",
        help="list of Ls (range of weights {-L,L}) to generate data, separated by SPACE",
    )
    parser.add_argument(
        "-n",
        "--number_of_inputs_per_neuron",
        required=True,
        type=int,
        nargs="+",
        help="Three integers for number of inputs to a single neuron to generate data (start, stop, step), separated by SPACE",
    )

    parser.add_argument(
        "-k",
        "--number_of_neurons_in_hidden_layer",
        type=int,
        required=True,
        nargs="+",
        help="Three integers for number of neurons in hidden layer to generate data (start, stop, step), separated by SPACE",
    )

    parser.add_argument(
        "-b",
        "--QBER",
        type=int,
        required=True,
        nargs="+",
        help="set list of QBERs to generate data about, separated by SPACE",
    )

    parser.add_argument(
        "-e",
        "--eve",
        type=int,
        default=0,
        help="number of Eve's machines",
    )

    parser.add_argument(
        "-f",
        "--filepath",
        type=str,
        default=DEFAULT_FILENAME,
        help="path to file to save data to [test /home/user/iterations.csv]",
    )
    return parser.parse_args()


def translate_args_to_simulator_parameters(args: Namespace) -> SimulatorParameters:
    weights_range = args.weights_range
    qber_values = args.QBER

    range_of_inputs_per_neuron = _assign_list_to_range(args.number_of_inputs_per_neuron)
    range_of_neurons_in_hidden_layer = _assign_list_to_range(
        args.number_of_neurons_in_hidden_layer
    )

    file_path = Path(args.file_path)

    return SimulatorParameters(
        weights_range,
        range_of_inputs_per_neuron,
        qber_values,
        range_of_neurons_in_hidden_layer,
        file_path,
        args.eve,
    )


def _assign_list_to_range(range_list: list[int]) -> Range:
    try:
        return Range(range_list[0], range_list[1], range_list[2])
    except IndexError:
        raise Exception(
            "Each range argument must contain exactly three integers separated by space."
        )