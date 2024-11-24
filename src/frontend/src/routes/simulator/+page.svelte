<!-- src/routes/simulation.svelte -->

<!--<script>-->
<!--    let isEve = false;-->
<!--    let eveMachines = 0;-->

<script>
    import { onMount } from 'svelte';
    import {redirect} from "@sveltejs/kit";
    let isEve = false;
    let eveMachines = 0;

    async function handleSubmit(event) {
        const url = `http://127.0.0.1:8000/simulator/start-simulation`;
        event.preventDefault();
        // let data = event.toString();
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
            if ( response.status === 200 ){
                try {
                    let returnData = await response.json();
                    console.log(returnData);
                    window.location.href= `simulator/status/${returnData.task_id}`;
                } catch (error) {
                    alert('Something went wrong please check currently-running simulations, or try again');
                }
            } else {
                alert('Error submitting form. Please try again.');
            }
        } catch (error) {
            console.error('Error submitting form:', error);
            alert('Error submitting form');
        }
    }
</script>

<!-- Page content -->
<div class="container-fluid">
    <div class="col-md-8">
    <h1 class="mt-4">Enter Simulation Parameters</h1>
    <form  on:submit={handleSubmit}>
        <!-- First Row of Inputs -->
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
        <!-- Second Row of Inputs -->
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
        <!-- Weights Range Input -->
        <div class="form-group">
            <label for="weights_range">Range of weights (comma-separated integers):</label>
            <input type="text" class="form-control" id="weights_range" name="weights_range" placeholder="1,2,3,4,5">
        </div>
        <!-- QBER Values Input -->
        <div class="form-group">
            <label for="qber_values">QBER values (comma-separated integers):</label>
            <input type="text" class="form-control" id="qber_values" name="qber_values" placeholder="6,7,8,9,10">
        </div>
        <!-- path input -->
        <div class="form-group">
            <label for="path">Result path:</label>
            <input type="text" class="form-control" id="path" name="path" placeholder="/home/user/results">
        </div>
        <!-- Is Eve Checkbox -->
        <div class="form-group form-check">
            <input type="checkbox" class="form-check-input" id="isEve" name="isEve" bind:checked={isEve}>
            <label class="form-check-label" for="isEve">Is Eve</label>
        </div>
        <!-- Eve Machines Section (conditionally shown) -->
        {#if isEve}
        <div class="form-group" id="eve_machines_div">
            <label for="eve_machines">Eve TPMs:</label>
            <input type="number" min="0" class="form-control" id="eve_machines" name="eve_machines" placeholder="Number of Eve machines" bind:value={eveMachines}>
        </div>
        {/if}
        <button type="submit" class="btn btn-primary">Start Simulation</button>
    </form>
    </div>
</div>
