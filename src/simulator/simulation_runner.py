import itertools
import numpy.typing as npt
import numpy as np
from numpy import signedinteger
from simulator.args_parser import SimulatorParameters
from simulator.common import (
    generate_single_tmp_weights,
    get_weights_with_error,
    generate_random_input,
)
from simulator.utils import write_row
from tree_parity_machine.tree_parity_machine import TPM, TPMBaseParameters
import time

def initialize_machines_for_synchronization(
    tpm_parameters: TPMBaseParameters,
    initial_weights_alice: npt.NDArray,
    initial_weights_bob: npt.NDArray,
) -> tuple[TPM, TPM]:
    alice = TPM(
        tmp_parameters=tpm_parameters,
        initial_weights=initial_weights_alice,
    )
    bob = TPM(
        tmp_parameters=tpm_parameters,
        initial_weights=initial_weights_bob,
    )
    return alice, bob

def update_weights(
    alice: TPM,
    bob: TPM,
    result: signedinteger,
    alice_weights: npt.NDArray,
    bob_weights: npt.NDArray,
) -> None:
    alice.update_result_node(result, alice_weights)
    bob.update_result_node(result, bob_weights)
    alice.update_weights()
    bob.update_weights()


def calculate_tpm_result(
    tpm: TPM, input_nodes: npt.NDArray
) -> tuple[signedinteger, npt.NDArray]:
    tpm.set_input_nodes(input_nodes)
    return tpm.calculate_TPM_results()

def update_eve_weights_if_possible(
    eves: list[TPM],
    eves_results: list[signedinteger],
    eves_weights: list[npt.NDArray],
    alice_result: signedinteger,
) -> int:
    eve_updated = 0
    for eve, eve_result, eve_weights in zip(eves, eves_results, eves_weights):
        if eve_result == alice_result:
            eve.update_result_node(eve_result, eve_weights)
            eve.update_weights()
            eve_updated += 1
    return eve_updated

def run_simulation(simulation_parameters: SimulatorParameters) -> bool:
    for parameters in itertools.product(*simulation_parameters.get_iteration_params()):
        (
            weights_value_limit,
            num_inputs_per_neuron,
            num_hidden_neurons,
            qber_value,
            ber_type,
            rep,
        ) = parameters
        tmp_parameters = TPMBaseParameters(
            num_hidden_neurons,
            num_inputs_per_neuron,
            weights_value_limit,
        )

        initial_weights_alice = generate_single_tmp_weights(tmp_parameters)
        initial_weights_bob, number_of_different_weights = get_weights_with_error(
            initial_weights_alice, weights_value_limit, qber_value, ber_type
        )

        attacker_data = []
        if (number_of_attacker_machines := simulation_parameters.eve) > 0:
            eves_weights = [
                generate_single_tmp_weights(tmp_parameters)
                for _ in range(number_of_attacker_machines)
            ]
            execution_time, runs, different_result, success_eve, eve_runs = simulate_tmp_synchronization_with_attacker(
                initial_weights_alice,
                initial_weights_bob,
                eves_weights,
                tmp_parameters,
            )
            attacker_data = [success_eve, eve_runs]
        else:
            execution_time, runs, different_result = simulate_tmp_synchronization(
                initial_weights_alice, initial_weights_bob, tmp_parameters
            )

        base_data = [
            weights_value_limit,
            num_inputs_per_neuron,
            num_hidden_neurons,
            qber_value,
            number_of_different_weights,
            ber_type,
            rep,
            different_result,
            execution_time,
            runs,
        ]

        data_row = base_data + attacker_data
        write_row(simulation_parameters.file_path, data_row)

    return True

def simulate_tmp_synchronization(
        initial_weights_alice: npt.NDArray,
        initial_weights_bob: npt.NDArray,
        tpm_parameters: TPMBaseParameters,
) -> tuple[float, int, int]:
    alice, bob = initialize_machines_for_synchronization(
        tpm_parameters, initial_weights_alice, initial_weights_bob
    )
    start_time = time.time()  # Async compatible timing
    runs, different_result = single_synchronization(alice, bob, tpm_parameters)
    execution_time = time.time() - start_time
    print(execution_time)
    return execution_time, runs, different_result


def single_synchronization(
        alice: TPM, bob: TPM, tpm_parameters: TPMBaseParameters
) -> tuple[int, int]:
    runs, different_result = 0, 0
    while not np.array_equal(alice.hidden_layer_weights, bob.hidden_layer_weights):
        runs += 1
        different_result += synchronization_step(
            alice,
            bob,
            tpm_parameters.number_of_neurons_in_hidden_layer,
            tpm_parameters.number_of_inputs_per_neuron,
        )
    return runs, different_result


def synchronization_step(
        alice: TPM, bob: TPM, num_hidden_neurons: int, num_inputs_per_neuron: int
) -> int:
    different_result = 0
    while True:
        input_nodes = generate_random_input(num_hidden_neurons, num_inputs_per_neuron)
        alice_result, alice_result_weights = calculate_tpm_result(alice, input_nodes)
        bob_result, bob_result_weights = calculate_tpm_result(bob, input_nodes)
        if alice_result == bob_result:
            update_weights(alice, bob, alice_result, alice_result_weights, bob_result_weights)
            break
        else:
            different_result += 1

    return different_result


def simulate_tmp_synchronization_with_attacker(
        initial_weights_alice: npt.NDArray,
        initial_weights_bob: npt.NDArray,
        eve_weights: list[npt.NDArray],
        tpm_parameters: TPMBaseParameters,
) -> tuple[float, int, int, int, int]:
    alice, bob = initialize_machines_for_synchronization(
        tpm_parameters, initial_weights_alice, initial_weights_bob
    )
    eves = [
        TPM(
            tmp_parameters=tpm_parameters,
            initial_weights=eve_weight,
        )
        for eve_weight in eve_weights
    ]
    start_time = time.time()
    runs, different_result, eve_runs = single_synchronization_with_attacker(
        alice, bob, eves, tpm_parameters
    )
    execution_time = time.time() - start_time

    print(execution_time)
    success_eve = sum(
        np.array_equal(eve.hidden_layer_weights, bob.hidden_layer_weights)
        for eve in eves
    )

    return execution_time, runs, different_result, success_eve, eve_runs


def single_synchronization_with_attacker(
        alice: TPM, bob: TPM, eves: list[TPM], tpm_parameters: TPMBaseParameters
) -> tuple[int, int, int]:
    runs, different_result, eve_runs = 0, 0, 0
    while not any(
            np.array_equal(alice.hidden_layer_weights, eve.hidden_layer_weights)
            for eve in eves
    ):
        if not np.array_equal(alice.hidden_layer_weights, bob.hidden_layer_weights):
            runs += 1
        eve_runs += 1
        different_result_in_step, eve_updated_in_step = synchronization_step_with_attackers(
            alice,
            bob,
            eves,
            tpm_parameters.number_of_neurons_in_hidden_layer,
            tpm_parameters.number_of_inputs_per_neuron,
        )
        different_result += different_result_in_step

    return runs, different_result, eve_runs


def synchronization_step_with_attackers(
        alice: TPM,
        bob: TPM,
        eves: list[TPM],
        num_hidden_neurons: int,
        num_inputs_per_neuron: int,
) -> tuple[int, int]:
    different_result, eve_updated = 0, 0
    while True:
        input_nodes = generate_random_input(num_hidden_neurons, num_inputs_per_neuron)
        alice_result, alice_result_weights = calculate_tpm_result(alice, input_nodes)
        bob_result, bob_result_weights = calculate_tpm_result(bob, input_nodes)
        eves_results, eves_result_weights = zip(
            *(calculate_tpm_result(eve, input_nodes) for eve in eves)
        )

        if alice_result == bob_result:
            update_weights(alice, bob, alice_result, alice_result_weights, bob_result_weights)
            eve_updated += update_eve_weights_if_possible(eves, eves_results, eves_result_weights, alice_result)
            break
        else:
            different_result += 1

    return different_result, eve_updated
