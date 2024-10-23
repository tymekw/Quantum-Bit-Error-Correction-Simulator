import argparse
from dataclasses import dataclass


DEFAULT_FILENAME = 'tmp_test_result.csv'

@dataclass
class SimulatorParameters:
    L: int
    N: list[int]
    QBER: list[int]
    K: list[int]
    filename: str
    is_eve: bool

def parse_arguments():
    parser = argparse.ArgumentParser(description="Simulate TPM to correct errors.")
    parser.add_argument(
        "-l",
        "--weights_range",
        type=int,
        nargs="+",
        help="list of Ls (range of weights {-L,L}) to generate data, separated by SPACE",
    )
    parser.add_argument(
        "-n",
        "--number_of_inputs_per_neuron",
        type=int,
        nargs="+",
        help="Ns (numbers of inputs to a single neuron) to generate data, [from to by] separated by SPACE",
    )

    parser.add_argument(
        "-k",
        "--number_of_neurons_in_hidden_layer",
        type=int,
        nargs="+",
        help="Ks (numbers of neurons in hidden layer) to generate data, [from to by] separated by SPACE",
    )

    parser.add_argument(
        "-b",
        "--QBER",
        type=int,
        nargs="+",
        help="set list of QBERs to generate data about, separated by SPACE",
    )

    parser.add_argument(
        "-e",
        "--eve",
        type=int,
        help="number of Eve's machines",
    )

    parser.add_argument(
        "-f",
        "--filename",
        type=str,
        help="name of file to save data to [test iterations.csv]",
    )
    return parser.parse_args()


def initialize_parameters(args):
    if args.weights_range:
        L = [int(i) for i in args.weights_range]
    if args.QBER:
        QBER = [int(i) for i in args.QBER]
    if args.number_of_inputs_per_neuron:
        N = [
            int(i)
            for i in range(
                args.number_of_inputs_per_neuron[0],
                args.number_of_inputs_per_neuron[1],
                args.number_of_inputs_per_neuron[2],
            )
        ]
    if args.number_of_neurons_in_hidden_layer:
        K = [
            int(i)
            for i in range(
                args.number_of_neurons_in_hidden_layer[0],
                args.number_of_neurons_in_hidden_layer[1],
                args.number_of_neurons_in_hidden_layer[2],
            )
        ]
    if args.filename and args.filename.endswith(".csv"):
        filename = args.filename
    else:
        filename = DEFAULT_FILENAME

    return SimulatorParameters(L, N, QBER, K, args.eve, filename)

