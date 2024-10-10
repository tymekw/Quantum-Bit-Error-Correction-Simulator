import numpy as np
import pytest

from tree_parity_machine.tree_parity_machine import TPM


class TestTPM:
    @pytest.mark.parametrize('current_hidden_layer_weights, expected_result, expected_hidden_layer_weights', (
            (np.array([0, 1]), -1, np.array([1, -1])),
            (np.array([1, 1]), 1, np.array([-1, -1]))
    ))
    def test_get_updated_result_and_hidden_layer_weights(
            self, current_hidden_layer_weights, expected_result, expected_hidden_layer_weights
    ):
        tpm = TPM(2, 2, 2, current_hidden_layer_weights)
        input_nodes = np.array([[-1, 1], [1, -1]])
        tpm.update_input_nodes(input_nodes)
        updated_result, hidden_layer_weights = tpm.get_updated_result_and_hidden_layer_weights()
        assert updated_result == expected_result
        assert np.array_equal(hidden_layer_weights, expected_hidden_layer_weights)

    def test_update_hidden_layer_weights(self):
        assert False

    def test_update_result(self):
        assert False

    def test_update_weights(self):
        assert False
