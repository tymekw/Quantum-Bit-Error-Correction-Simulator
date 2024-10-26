import itertools
import time
import numpy.typing as npt

import numpy as np
from numpy import signedinteger

from simulator.args_parser import (
    SimulatorParameters,
)
from simulator.common import (
    generate_single_tmp_weights,
    get_weights_with_error,
    generate_random_input,
)
from simulator.utils import write_row
import math
from tree_parity_machine.tree_parity_machine import TPM, TMPBaseParameters


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
            execution_time, runs, tau_not_hit, success_eve, eve_runs = (
                simulate_tmp_synchronization_with_attacker(
                    initial_weights_alice,
                    initial_weights_bob,
                    eves_weights,
                    tmp_parameters,
                )
            )
            data_row = [
                weights_value_limit,
                number_of_inputs_per_neuron,
                number_of_neurons_in_hidden_layer,
                qber_value,
                number_of_different_weights,
                ber_type,
                rep,
                tau_not_hit,
                execution_time,
                runs,
                success_eve,
                eve_runs,
            ]
        else:
            execution_time, runs, tau_not_hit = simulate_tmp_synchronization(
                initial_weights_alice, initial_weights_bob, tmp_parameters
            )
            data_row = [
                weights_value_limit,
                number_of_inputs_per_neuron,
                number_of_neurons_in_hidden_layer,
                qber_value,
                number_of_different_weights,
                ber_type,
                rep,
                tau_not_hit,
                execution_time,
                runs,
            ]

        write_row(simulation_parameters.file_path, data_row)


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
        input_nodes = generate_random_input(
            tmp_parameters.number_of_neurons_in_hidden_layer,
            tmp_parameters.number_of_inputs_per_neuron,
        )
        alice_result, alice_result_weights = calculate_tpm_result(alice, input_nodes)
        bob_result, bob_result_weights = calculate_tpm_result(bob, input_nodes)

        while alice_result != bob_result:
            tau_not_hit += 1
            input_nodes = generate_random_input(
                tmp_parameters.number_of_neurons_in_hidden_layer,
                tmp_parameters.number_of_inputs_per_neuron,
            )
            alice_result, alice_result_weights = calculate_tpm_result(
                alice, input_nodes
            )
            bob_result, bob_result_weights = calculate_tpm_result(bob, input_nodes)

        alice.update_result_node(alice_result, alice_result_weights)
        bob.update_result_node(bob_result, bob_result_weights)
        alice.update_weights()
        bob.update_weights()

    execution_time = time.time() - start_time
    print(execution_time)
    return execution_time, runs, tau_not_hit


def calculate_tpm_result(
    tpm: TPM, input_nodes: npt.NDArray
) -> tuple[signedinteger, npt.NDArray]:
    tpm.set_input_nodes(input_nodes)
    return tpm.calculate_TPM_results()


def simulate_tmp_synchronization_with_attacker(
    initial_weights_alice, initial_weights_bob, eve_weights, tmp_parameters
):
    alice = TPM(
        tmp_parameters=tmp_parameters,
        initial_weights=initial_weights_alice,
    )
    bob = TPM(
        tmp_parameters=tmp_parameters,
        initial_weights=initial_weights_bob,
    )
    eves = [
        TPM(
            tmp_parameters=tmp_parameters,
            initial_weights=eve_weight,
        )
        for eve_weight in eve_weights
    ]

    runs = 0
    tau_not_hit = 0
    start_time = time.time()
    runs_required = math.inf
    eve_updated = 0
    eve_runs = 0
    while not any(
        np.array_equal(alice.hidden_layer_weights, eve.hidden_layer_weights)
        for eve in eves
    ):
        if np.array_equal(alice.hidden_layer_weights, bob.hidden_layer_weights):
            runs_required = min(runs, runs_required)
        else:
            runs += 1
        eve_runs += 1
        input_nodes = generate_random_input(
            tmp_parameters.number_of_neurons_in_hidden_layer,
            tmp_parameters.number_of_inputs_per_neuron,
        )
        alice_result, alice_result_weights = calculate_tpm_result(alice, input_nodes)
        bob_result, bob_result_weights = calculate_tpm_result(bob, input_nodes)

        eves_results, eves_result_weights = zip(
            *(calculate_tpm_result(eve, input_nodes) for eve in eves)
        )

        while alice_result != bob_result:
            tau_not_hit += 1
            input_nodes = generate_random_input(
                tmp_parameters.number_of_neurons_in_hidden_layer,
                tmp_parameters.number_of_inputs_per_neuron,
            )
            alice_result, alice_result_weights = calculate_tpm_result(
                alice, input_nodes
            )
            bob_result, bob_result_weights = calculate_tpm_result(bob, input_nodes)
            eves_results, eves_result_weights = zip(
                *(calculate_tpm_result(eve, input_nodes) for eve in eves)
            )

        alice.update_result_node(alice_result, alice_result_weights)
        bob.update_result_node(bob_result, bob_result_weights)
        alice.update_weights()
        bob.update_weights()

        for eve, eve_result, eve_result_weight in zip(
            eves, eves_results, eves_result_weights
        ):
            if eve_result == alice_result:
                eve.update_result_node(eve_result, eve_result_weight)
                eve.update_weights()
                eve_updated += 1

        if np.array_equal(alice.hidden_layer_weights, bob.hidden_layer_weights):
            runs_required = min(runs, runs_required)

    execution_time = time.time() - start_time
    print(execution_time)
    success_eve = sum(
        np.array_equal(eve.hidden_layer_weights, bob.hidden_layer_weights)
        for eve in eves
    )

    return execution_time, runs, tau_not_hit, success_eve, eve_runs
