import argparse


class TPMSimulatorParser:
    def __init__(self):
        self._parser = argparse.ArgumentParser(description='TPM used to correct errors arisen during QKD.')
        self._add_arguments()
        self._args = self._parser.parse_args()

    def _add_arguments(self) -> None:
        self._parser.add_argument(
            "-l",
            "--weights_range",
            type=int,
            nargs="+",
            help="list of Ls (range of weights {-L,L}) to generate data, separated by SPACE",
            required=True
        )
        self._parser.add_argument(
            "-n",
            "--number_of_inputs_per_neuron",
            type=int,
            nargs="+",
            help="Ns (numbers of inputs to a single neuron) to generate data, [from to by] separated by SPACE",
            required=True
        )

        self._parser.add_argument(
            "-k",
            "--number_of_neurons_in_hidden_layer",
            type=int,
            nargs="+",
            help="Ks (numbers of neurons in hidden layer) to generate data, [from to by] separated by SPACE",
            required=True
        )

        self._parser.add_argument(
            "-b",
            "--QBER",
            type=int,
            nargs="+",
            help="set list of QBERs to generate data about, separated by SPACE",
            required=True
        )

        self._parser.add_argument(
            "-e",
            "--eve",
            type=int,
            help="number of Eve's machines",
        )

        self._parser.add_argument(
            "-f",
            "--filename",
            type=str,
            help="name of file to save data to",
            default='simulation_results.csv'
        )

    @property
    def weights_range(self) -> list[int]:
        return [int(i) for i in self._args.weights_range]

    @property
    def qber(self) -> list[int]:
        return [int(i) for i in self._args.QBER]

    @property
    def number_of_inputs_per_neuron(self) -> list[int]:
        return [
            int(i) for i in range(
                self._args.number_of_inputs_per_neuron[0],
                self._args.number_of_inputs_per_neuron[1],
                self._args.number_of_inputs_per_neuron[2]
            )
        ]

    @property
    def number_of_neurons_in_hidden_layer(self) -> list[int]:
        return [
            int(i) for i in range(
                self._args.number_of_neurons_in_hidden_layer[0],
                self._args.number_of_neurons_in_hidden_layer[1],
                self._args.number_of_neurons_in_hidden_layer[2]
            )
        ]

    @property
    def filename(self) -> str:
        return self._args.filename

    def is_eve_simulation(self) -> bool:
        return bool(self._args.eve)
