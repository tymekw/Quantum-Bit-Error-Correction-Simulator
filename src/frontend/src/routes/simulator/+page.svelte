<!-- src/routes/simulation.svelte -->

<script>
    let isEve = false;
    let eveMachines = 0;
</script>

<!-- Page-specific head elements -->
<svelte:head>
    <title>Simulation Parameters</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
    </style>
</svelte:head>

<!-- Page content -->
<div class="container">
    <h1 class="mt-4">Enter Simulation Parameters</h1>
    <form id="simulationForm">
        <!-- First Row of Inputs -->
        <div class="row mb-3">
            <div class="col">
                <label for="range_of_inputs_per_neuron_start" class="form-label">range_of_inputs_per_neuron_start Start:</label>
                <input type="number" class="form-control" id="range_of_inputs_per_neuron_start" name="range_of_inputs_per_neuron_start" placeholder="Start">
            </div>
            <div class="col">
                <label for="range_of_inputs_per_neuron_stop" class="form-label">range_of_inputs_per_neuron_stop Stop:</label>
                <input type="number" class="form-control" id="range_of_inputs_per_neuron_stop" name="range_of_inputs_per_neuron_stop" placeholder="Stop">
            </div>
            <div class="col">
                <label for="range_of_inputs_per_neuron_step" class="form-label">range_of_inputs_per_neuron_step Step:</label>
                <input type="number" class="form-control" id="range_of_inputs_per_neuron_step" name="range_of_inputs_per_neuron_step" placeholder="Step">
            </div>
        </div>
        <!-- Second Row of Inputs -->
        <div class="row mb-3">
            <div class="col">
                <label for="range_of_neurons_in_hidden_layer_start" class="form-label">range_of_neurons_in_hidden_layer Start:</label>
                <input type="number" class="form-control" id="range_of_neurons_in_hidden_layer_start" name="range_of_neurons_in_hidden_layer_start" placeholder="Start">
            </div>
            <div class="col">
                <label for="range_of_neurons_in_hidden_layer_stop" class="form-label">range_of_neurons_in_hidden_layer Stop:</label>
                <input type="number" class="form-control" id="range_of_neurons_in_hidden_layer_stop" name="range_of_neurons_in_hidden_layer_stop" placeholder="Stop">
            </div>
            <div class="col">
                <label for="range_of_neurons_in_hidden_layer_step" class="form-label">range_of_neurons_in_hidden_layer Step:</label>
                <input type="number" class="form-control" id="range_of_neurons_in_hidden_layer_step" name="range_of_neurons_in_hidden_layer_step" placeholder="Step">
            </div>
        </div>
        <!-- Weights Range Input -->
        <div class="form-group">
            <label for="weights_range">weights_range (comma-separated integers):</label>
            <input type="text" class="form-control" id="weights_range" name="weights_range" placeholder="e.g., 1,2,3,4,5">
        </div>
        <!-- QBER Values Input -->
        <div class="form-group">
            <label for="qber_values">qber_values (comma-separated integers):</label>
            <input type="text" class="form-control" id="qber_values" name="qber_values" placeholder="e.g., 6,7,8,9,10">
        </div>
        <!-- path input -->
        <div class="form-group">
            <label for="path">result path:</label>
            <input type="text" class="form-control" id="path" name="path" placeholder="e.g., /home/user/results">
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
            <input type="number" class="form-control" id="eve_machines" name="eve_machines" placeholder="Number of Eve machines" bind:value={eveMachines}>
        </div>
        {/if}
        <button type="button" class="btn btn-primary">Submit</button>
    </form>
</div>
