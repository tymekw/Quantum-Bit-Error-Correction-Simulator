import itertools
import time

import numpy as np

from simulator.args_parser import (
    parse_input_arguments,
    translate_args_to_simulator_parameters,
    SimulatorParameters,
)
from simulator.common import (
    generate_single_tmp_weights,
    get_weights_with_error,
    generate_random_input,
)

from tree_parity_machine.tree_parity_machine import TPM, TMPBaseParameters

REPS_FOR_STATS = 6


def main():
    args = parse_input_arguments()
    simulator_params = translate_args_to_simulator_parameters(args)
    run_simulation(simulator_params)


def run_simulation(simulation_parameters: SimulatorParameters) -> None:
    for (
        weights_value_limit,
        number_of_inputs_per_neuron,
        number_of_neurons_in_hidden_layer,
        qber_value,
        ber_type,
        rep,
    ) in itertools.product(*simulation_parameters.get_iteration_params()):
        tmp_parameters = TMPBaseParameters(
            number_of_neurons_in_hidden_layer,
            number_of_inputs_per_neuron,
            weights_value_limit,
        )
        initial_weights_alice = generate_single_tmp_weights(tmp_parameters)
        initial_weights_bob, number_of_different_weights = get_weights_with_error(
            initial_weights_alice, weights_value_limit, qber_value, ber_type
        )

        print(
            f"l:{weights_value_limit}, n:{number_of_inputs_per_neuron}, k:{number_of_neurons_in_hidden_layer}, ber:{qber_value}, ber_type:{ber_type}, rep:{rep}"
        )

        if number_of_attacker_machines := simulation_parameters.eve:
            eves_weights = [
                generate_single_tmp_weights(tmp_parameters)
                for _ in range(number_of_attacker_machines)
            ]
            simulate_tmp_synchronization_with_attacker()
        else:
            simulate_tmp_synchronization(
                initial_weights_alice, initial_weights_bob, tmp_parameters
            )


def simulate_tmp_synchronization(
    initial_weights_alice, initial_weights_bob, tmp_parameters
):
    alice = TPM(
        tmp_parameters=tmp_parameters,
        initial_weights=initial_weights_alice,
    )
    bob = TPM(
        tmp_parameters=tmp_parameters,
        initial_weights=initial_weights_bob,
    )
    runs = 0
    tau_not_hit = 0
    start_time = time.time()
    while not np.array_equal(alice.hidden_layer_weights, bob.hidden_layer_weights):
        runs += 1
        X = generate_random_input(
            tmp_parameters.number_of_neurons_in_hidden_layer,
            tmp_parameters.number_of_inputs_per_neuron,
        )
        alice.input_nodes = X
        bob.input_nodes = X
        a_tau, a_sigma = alice.calculate_TPM_results()
        b_tau, b_sigma = bob.calculate_TPM_results()
        while a_tau != b_tau:
            tau_not_hit += 1
            X = generate_random_input(
                tmp_parameters.number_of_neurons_in_hidden_layer,
                tmp_parameters.number_of_inputs_per_neuron,
            )
            alice.input_nodes = X
            bob.input_nodes = X
            a_tau, a_sigma = alice.calculate_TPM_results()
            b_tau, b_sigma = bob.calculate_TPM_results()
        alice.result = a_tau
        alice.result_weights = a_sigma
        bob.result = a_tau
        bob.result_weights = a_sigma
        alice.update_weights()
        bob.update_weights()
    execution_time = time.time() - start_time
    print(execution_time)


def simulate_tmp_synchronization_with_attacker():
    pass


if __name__ == "__main__":
    main()
#
#
# BER_TYPES = ("random", "bursty")
# if not EVE:
#     for l, n, k, ber, ber_type, rep in itertools.product(
#         L, N, K, QBER, BER_TYPES, range(REPS_FOR_STATS)
#     ):
#         initial_weights_alice, initial_weights_bob, different_weights = (
#             generate_weights(ber, ber_type, k, n, l)
#         )
#         print(f"l:{l}, n:{n}, k:{k}, ber:{ber}, ber_type:{ber_type}, rep:{rep}")
#         alice = TPM(n, k, l, initial_weights_alice)
#         bob = TPM(n, k, l, initial_weights_bob)
#         runs = 0
#         tau_not_hit = 0
#         start_time = time.time()
#         while not np.array_equal(alice.hidden_layer_weights, bob.hidden_layer_weights):
#             runs += 1
#             X = generate_random_input(k, n)
#             alice.input_nodes = X
#             bob.input_nodes = X
#             a_tau, a_sigma = alice.calculate_TPM_results()
#             b_tau, b_sigma = bob.calculate_TPM_results()
#             while a_tau != b_tau:
#                 tau_not_hit += 1
#                 X = generate_random_input(k, n)
#                 alice.input_nodes = X
#                 bob.input_nodes = X
#                 a_tau, a_sigma = alice.calculate_TPM_results()
#                 b_tau, b_sigma = bob.calculate_TPM_results()
#             alice.result = a_tau
#             alice.result_weights = a_sigma
#             bob.result = a_tau
#             bob.result_weights = a_sigma
#             alice.update_weights()
#             bob.update_weights()
#
#         execution_time = time.time() - start_time
#         data_row = [
#             l,
#             n,
#             k,
#             ber,
#             different_weights,
#             ber_type,
#             rep,
#             tau_not_hit,
#             execution_time,
#             runs,
#         ]
#
#         write_row(file_path, data_row)
# else:
#     for l, n, k, ber, ber_type, rep in itertools.product(
#         L, N, K, QBER, BER_TYPES, range(REPS_FOR_STATS)
#     ):
#         initial_weights_alice, initial_weights_bob, different_weights = (
#             generate_weights(ber, ber_type, k, n, l)
#         )
#         eves_weights = [generate_weights(ber, ber_type, k, n, l)[0] for _ in range(EVE)]
#
#         print(f"l:{l}, n:{n}, k:{k}, ber:{ber}, ber_type:{ber_type}, rep:{rep}")
#         alice = TPM(n, k, l, initial_weights_alice)
#         bob = TPM(n, k, l, initial_weights_bob)
#         eves = [TPM(n, k, l, eves_weights[i]) for i in range(EVE)]
#         runs_required = math.inf
#         runs = 0
#         eve_runs = 0
#         tau_not_hit = 0
#         start_time = time.time()
#         eve_updated = 0
#         success_eve = 0
#         while not any(
#             np.array_equal(alice.hidden_layer_weights, eve.hidden_layer_weights)
#             for eve in eves
#         ):
#             if np.array_equal(alice.hidden_layer_weights, bob.hidden_layer_weights):
#                 runs_required = min(runs, runs_required)
#             else:
#                 runs += 1
#
#             eve_runs += 1
#             X = generate_random_input(k, n)
#             alice.set_X(X)
#             bob.set_X(X)
#             a_tau, a_sigma = alice.calculate_TPM_results()
#             b_tau, b_sigma = bob.calculate_TPM_results()
#             [eve.set_X(X) for eve in eves]
#             eves_taus = [eve.calculate_TPM_results()[0] for eve in eves]
#             eves_sigmas = [eve.calculate_TPM_results()[1] for eve in eves]
#
#             while a_tau != b_tau:
#                 tau_not_hit += 1
#                 X = generate_random_input(k, n)
#                 alice.set_X(X)
#                 bob.set_X(X)
#                 [eve.set_X(X) for eve in eves]
#                 a_tau, a_sigma = alice.calculate_TPM_results()
#                 b_tau, b_sigma = bob.calculate_TPM_results()
#                 eves_taus = [eve.calculate_TPM_results()[0] for eve in eves]
#                 eves_sigmas = [eve.calculate_TPM_results()[1] for eve in eves]
#
#             for eve_idx in range(EVE):
#                 if eves_taus[eve_idx] == a_tau:
#                     eves[eve_idx].set_tau(a_tau)
#                     eves[eve_idx].set_sigma(a_sigma)
#                     eves[eve_idx].update_weights()
#                     eve_updated += 1
#
#             alice.set_tau(a_tau)
#             alice.set_sigma(a_sigma)
#             bob.set_tau(a_tau)
#             bob.set_sigma(a_sigma)
#             alice.update_weights()
#             bob.update_weights()
#
#         execution_time = time.time() - start_time
#         for eve_idx in range(EVE):
#             if np.array_equal(
#                 eves[eve_idx].hidden_layer_weights, bob.hidden_layer_weights
#             ):
#                 success_eve += 1
#         data_row = [
#             l,
#             n,
#             k,
#             ber,
#             different_weights,
#             ber_type,
#             rep,
#             tau_not_hit,
#             execution_time,
#             runs_required,
#             success_eve,
#             eve_runs,
#         ]
#         print("#" * 100)
#         print(f"Eve sucessfull: {success_eve}")
#         print(f"Eve runs: {eve_runs}")
#         print(f"Alcie Bob runs: {runs_required}")
#
#         write_row(file_path, data_row)
