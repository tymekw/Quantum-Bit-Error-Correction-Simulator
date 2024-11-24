<script>
    let isEve = false;
    let eveMachines = 0;

    async function handleSubmit(event) {
        const url = `http://127.0.0.1:8000/simulator/start-simulation`;
        event.preventDefault();
        const formData = new FormData(event.target);

        const data = {
            range_of_inputs_per_neuron: {
                start: parseInt(formData.get('range_of_inputs_per_neuron_start')),
                stop: parseInt(formData.get('range_of_inputs_per_neuron_stop')),
                step: parseInt(formData.get('range_of_inputs_per_neuron_step'))
            },
            range_of_neurons_in_hidden_layer: {
                start: parseInt(formData.get('range_of_neurons_in_hidden_layer_start')),
                stop: parseInt(formData.get('range_of_neurons_in_hidden_layer_stop')),
                step: parseInt(formData.get('range_of_neurons_in_hidden_layer_step'))
            },
            weights_range: formData.get('weights_range').split(',').map(Number),
            qber_values: formData.get('qber_values').split(',').map(Number),
            file_path: formData.get('path') || null,
            eve: formData.get('eve_machines') ? parseInt(formData.get('eve_machines')) || 0 : 0
        };

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            if (response.status === 200) {
                let returnData = await response.json();
                console.log(returnData);
                window.location.href = `simulator/status/${returnData.task_id}`;
            } else {
                alert('Error submitting form. Please try again.');
            }
        } catch (error) {
            console.error('Error submitting form:', error);
            alert('Error submitting form');
        }
    }
</script>

<style>
    .container-fluid {
        padding: 2rem;
    }

    .param-group {
        background-color: #f4f4f4;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }

    .form-label {
        font-weight: bold;
    }

    .form-control {
        padding: 0.8rem;
        font-size: 1rem;
        border-radius: 5px;
        border: 1px solid #ccc;
        transition: border 0.3s ease;
        background-color: #fff;
    }

    .form-control:focus {
        border-color: #6c757d;
        outline: none;
    }

    .btn-gray {
        background-color: #6c757d;
        border-color: #6c757d;
        padding: 0.8rem 1.5rem;
        font-size: 1.1rem;
        border-radius: 5px;
        color: white;
        cursor: pointer;
        text-align: center;
    }

    .btn-gray:hover {
        background-color: #5a6369;
        border-color: #545b62;
    }

    .row {
        display: flex;
        gap: 1rem;
    }

    .col {
        flex: 1;
    }

    /* Custom toggle switch */
    .toggle-switch {
        display: inline-flex;
        align-items: center;
    }

    .toggle-switch input {
        display: none;
    }

    .toggle-switch .switch {
        position: relative;
        width: 50px;
        height: 24px;
        background-color: #ccc;
        border-radius: 50px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }

    .toggle-switch .switch::before {
        content: '';
        position: absolute;
        top: 2px;
        left: 2px;
        width: 20px;
        height: 20px;
        background-color: #fff;
        border-radius: 50%;
        transition: transform 0.3s ease;
    }

    .toggle-switch input:checked + .switch {
        background-color: #4caf50;
    }

    .toggle-switch input:checked + .switch::before {
        transform: translateX(26px);
    }

    .form-check-label {
        font-weight: normal;
        margin-left: 10px;
    }
</style>

<div class="container-fluid">
    <h1 class="mt-4">Enter Simulation Parameters</h1>
    <form on:submit={handleSubmit}>
        <!-- First Row of Inputs -->
        <div class="param-group">
            <div class="row mb-3">
                <div class="col">
                    <label for="range_of_inputs_per_neuron_start" class="form-label">Range of inputs per neuron (START):</label>
                    <input type="number" min="1" class="form-control" id="range_of_inputs_per_neuron_start" name="range_of_inputs_per_neuron_start" placeholder="Start">
                </div>
                <div class="col">
                    <label for="range_of_inputs_per_neuron_stop" class="form-label">Range of inputs per neuron (STOP):</label>
                    <input type="number" min="1" class="form-control" id="range_of_inputs_per_neuron_stop" name="range_of_inputs_per_neuron_stop" placeholder="Stop">
                </div>
                <div class="col">
                    <label for="range_of_inputs_per_neuron_step" class="form-label">Range of inputs per neuron (STEP):</label>
                    <input type="number" min="1" class="form-control" id="range_of_inputs_per_neuron_step" name="range_of_inputs_per_neuron_step" placeholder="Step">
                </div>
            </div>
        </div>

        <!-- Second Row of Inputs -->
        <div class="param-group">
            <div class="row mb-3">
                <div class="col">
                    <label for="range_of_neurons_in_hidden_layer_start" class="form-label">Range of neurons in hidden layer (START):</label>
                    <input type="number" min="1" class="form-control" id="range_of_neurons_in_hidden_layer_start" name="range_of_neurons_in_hidden_layer_start" placeholder="Start">
                </div>
                <div class="col">
                    <label for="range_of_neurons_in_hidden_layer_stop" class="form-label">Range of neurons in hidden layer (STOP):</label>
                    <input type="number" min="1" class="form-control" id="range_of_neurons_in_hidden_layer_stop" name="range_of_neurons_in_hidden_layer_stop" placeholder="Stop">
                </div>
                <div class="col">
                    <label for="range_of_neurons_in_hidden_layer_step" class="form-label">Range of neurons in hidden layer (STEP):</label>
                    <input type="number" min="1" class="form-control" id="range_of_neurons_in_hidden_layer_step" name="range_of_neurons_in_hidden_layer_step" placeholder="Step">
                </div>
            </div>
        </div>

        <!-- Weights Range Input -->
        <div class="param-group">
            <label for="weights_range" class="form-label">Range of weights (comma-separated integers):</label>
            <input type="text" class="form-control" id="weights_range" name="weights_range" placeholder="1,2,3,4,5">
        </div>

        <!-- QBER Values Input -->
        <div class="param-group">
            <label for="qber_values" class="form-label">QBER values (comma-separated integers):</label>
            <input type="text" class="form-control" id="qber_values" name="qber_values" placeholder="6,7,8,9,10">
        </div>

        <!-- Path Input -->
        <div class="param-group">
            <label for="path" class="form-label">Result path:</label>
            <input type="text" class="form-control" id="path" name="path" placeholder="/home/user/results">
        </div>

        <!-- Is Eve Toggle Switch -->
        <div class="param-group">
            <label class="form-check-label" for="isEve">Is Eve</label>
            <div class="toggle-switch">
                <input type="checkbox" id="isEve" name="isEve" bind:checked={isEve}>
                <label class="switch" for="isEve"></label>
            </div>
        </div>

        <!-- Eve Machines Section (conditionally shown) -->
        {#if isEve}
        <div class="param-group" id="eve_machines_div">
            <label for="eve_machines" class="form-label">Eve TPMs:</label>
            <input type="number" min="0" class="form-control" id="eve_machines" name="eve_machines" placeholder="Number of Eve machines" bind:value={eveMachines}>
        </div>
        {/if}

        <button type="submit" class="btn-gray">Start Simulation</button>
    </form>
</div>
