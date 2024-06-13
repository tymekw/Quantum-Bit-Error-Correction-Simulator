import csv
import itertools

from tpm.simulator_tmp.parser import TPMSimulatorParser

DEFAULT_SIMULATION_ROWS = ["L", "N", "K", "QBER", "ERRORS", "QBER_TYPE", "REP", "TAU_MISSES", "TIME", "REPETITIONS"]
EVE_SIMULATION_ROWS = DEFAULT_SIMULATION_ROWS + ["EVE_SUCCESS", "EVE_REQUIRED"]


class TPMSimulator:
    def __init__(self, parser: TPMSimulatorParser):
        self._args_parser: TPMSimulatorParser = parser

    def _write_row(self, row_data: list) -> None:
        with open(self._args_parser.filename, 'a+', newline='') as file:
            writer = csv.writer(file, delimeter=';')
            writer.writerow(row_data)

    def run_simulation(self) -> None:
        if self._args_parser.is_eve_simulation:
            self._run_default_simulation()  # ToDo EVE
        else:
            self._run_default_simulation()

    def _get_loop_parameters(self) -> tuple[int, int, int, int, BerType, int]:
        yield from itertools.product(
            self._args_parser.weights_range,
            self._args_parser.number_of_inputs_per_neuron,
            self._args_parser.number_of_neurons_in_hidden_layer,
            self._args_parser.qber,
            BER_TYPES,
            range(REPS_FOR_STATS)
        )

    def _run_default_simulation(self) -> None:
        self._write_row(DEFAULT_SIMULATION_ROWS)
        for l, n, k, ber, ber_type, rep in self._get_loop_parameters():
            initial_weights_alice, initial_weights_bob, different_weights = generate_weights(
                ber, ber_type, k, n, l
            )
            print(f'l:{l}, n:{n}, k:{k}, ber:{ber}, ber_type:{ber_type}, rep:{rep}')
            alice = TPM(n, k, l, initial_weights_alice)
            bob = TPM(n, k, l, initial_weights_bob)
            runs = 0
            tau_not_hit = 0
            start_time = time.time()
            while not np.array_equal(alice.W, bob.W):
                runs += 1
                X = generate_random_input(k, n)
                alice.set_X(X)
                bob.set_X(X)
                a_tau, a_sigma = alice.calculate_TPM_results()
                b_tau, b_sigma = bob.calculate_TPM_results()
                while a_tau != b_tau:
                    tau_not_hit += 1
                    X = generate_random_input(k, n)
                    alice.set_X(X)
                    bob.set_X(X)
                    a_tau, a_sigma = alice.calculate_TPM_results()
                    b_tau, b_sigma = bob.calculate_TPM_results()
                alice.set_tau(a_tau)
                alice.set_sigma(a_sigma)
                bob.set_tau(a_tau)
                bob.set_sigma(a_sigma)
                alice.update_weights()
                bob.update_weights()

            execution_time = time.time() - start_time
            data_row = [l, n, k, ber, different_weights, ber_type, rep, tau_not_hit, execution_time, runs]

            self._write_row(data_row)