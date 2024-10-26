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
            simulate_tmp_synchronization_with_attacker()
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
        (alice_result, alice_result_weights), (bob_result, bob_result_weights) = (
            calculate_results(alice, bob, input_nodes)
        )
        while alice_result != bob_result:
            tau_not_hit += 1
            input_nodes = generate_random_input(
                tmp_parameters.number_of_neurons_in_hidden_layer,
                tmp_parameters.number_of_inputs_per_neuron,
            )
            (alice_result, alice_result_weights), (bob_result, bob_result_weights) = (
                calculate_results(alice, bob, input_nodes)
            )

        alice.update_result_node(alice_result, alice_result_weights)
        bob.update_result_node(bob_result, bob_result_weights)
        alice.update_weights()
        bob.update_weights()

    execution_time = time.time() - start_time
    print(execution_time)
    return execution_time, runs, tau_not_hit


def calculate_results(
    alice: TPM, bob: TPM, input_nodes: npt.NDArray
) -> tuple[tuple[signedinteger, npt.NDArray], tuple[signedinteger, npt.NDArray]]:
    alice.set_input_nodes(input_nodes)
    bob.set_input_nodes(input_nodes)
    alice_result, alice_result_weights = alice.calculate_TPM_results()
    bob_result, bob_result_weights = bob.calculate_TPM_results()
    return (alice_result, alice_result_weights), (bob_result, bob_result_weights)


def simulate_tmp_synchronization_with_attacker():
    pass
