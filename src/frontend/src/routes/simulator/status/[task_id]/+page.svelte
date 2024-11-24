<script>
    import { onMount } from 'svelte';
    export let data;
    export let error;

    let simulationData = data?.data || null;
    let task_id = simulationData?.task_id;

    const fetchData = async () => {
        if (task_id == null || simulationData.status !== 'running') return;

        try {
            const response = await fetch(`http://127.0.0.1:8000/simulator/status/${task_id}`);
            if (!response.ok) throw new Error('Failed to fetch data');
            simulationData = await response.json();
            task_id = simulationData.task_id;
            error = null;
        } catch (err) {
            error = err.message;
            console.error("Fetch error:", err);
        }
    };

    const cancelTask = async () => {
        if (task_id == null || simulationData.status !== 'running') return;

        try {
            const response = await fetch(`http://127.0.0.1:8000/simulator/cancel-simulation/${task_id}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
            });

            if (!response.ok) throw new Error('Failed to cancel task');
            await fetchData();
        } catch (err) {
            error = err.message;
            console.error("Cancel error:", err);
        }
    };

    onMount(() => {
        fetchData();
        const interval = setInterval(fetchData, 10000);
        return () => clearInterval(interval);
    });
</script>
<style>
    .status {
        display: flex;
        align-items: center;
        gap: 15px;
        font-weight: bold;
        padding: 12px;
        border-radius: 8px;
        background-color: #f8f9fa;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
        max-width: 600px;
    }

    .status.not_started {
        color: #6c757d;
    }

    .status.started {
        color: #007bff;
    }

    .status.running {
        color: #28a745;
    }

    .status.stopping {
        color: #fd7e14;
    }

    .status.cancelled {
        color: #dc3545;
    }

    .status.finished {
        color: #155724;
    }

    .spinner {
        border: 4px solid rgba(0, 255, 0, 0.3);
        border-top: 4px solid green;
        border-radius: 50%;
        width: 25px;
        height: 25px;
        animation: spin 1s linear infinite;
    }

    .parameters {
        font-weight: normal;
        margin-top: 1rem;
        max-width: 600px;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .result-file {
        padding: 12px;
        background-color: #e9ecef;
        border-radius: 8px;
        margin-top: 1.5rem;
        max-width: 600px;

    }

    .result-file a {
        color: #fff;
        text-decoration: none;
        background-color: #6c757d;
        padding: 10px 18px;
        border-radius: 4px;
        font-size: 1rem;
        transition: background-color 0.3s ease;
    }

    .result-file a:hover {
        background-color: #5a6268;
    }

    .parameter-item {
        display: flex;
        flex-direction: column;
        gap: 8px;
        margin-bottom: 12px;
    }

    .parameter-item strong {
        font-weight: bold;
        color: #343a40;
    }

    .parameter-item .value {
        display: block;
        color: #495057;
        font-size: 0.95rem;
    }
</style>

<div class="container-fluid">
    <div class="col-md-8">
        {#if error}
            <p class="text-danger">Error: {error}</p>
        {:else if (simulationData && task_id != null)}
            <h1 class="mb-4">Simulation Status ID: {task_id}</h1>

            <div class="status {simulationData.status}">
                {#if simulationData.status === 'running'}
                    <div class="spinner"></div>
                {/if}
                <span>
                    {#if simulationData.status === 'not_started'}
                        Simulation not started.
                    {:else if simulationData.status === 'started'}
                        Simulation has started.
                    {:else if simulationData.status === 'running'}
                        Simulation is running...
                    {:else if simulationData.status === 'stopping'}
                        Simulation is stopping...
                    {:else if simulationData.status === 'cancelled'}
                        Simulation was cancelled.
                    {:else if simulationData.status === 'finished'}
                        Simulation has finished.
                    {/if}
                </span>

                {#if simulationData.status === 'running'}
                    <button class="btn btn-danger ml-3" on:click={cancelTask}>Cancel simulation</button>
                {/if}
            </div>

            {#each Object.entries(simulationData.parameters) as [key, value]}
                <div class="parameters status">
                    <div class="parameter-item">
                        {#if key === 'weights_range'}
                            <strong>Selected weights</strong>
                            <span class="value">{value}</span>
                        {:else if key === 'range_of_inputs_per_neuron'}
                            <strong>Selected range of inputs per single neuron</strong>
                            <span class="value">start: {value.start}, stop: {value.stop}, step: {value.step}</span>
                        {:else if key === 'qber_values'}
                            <strong>Selected QBER values</strong>
                            <span class="value">{value}</span>
                        {:else if key === 'range_of_neurons_in_hidden_layer'}
                            <strong>Selected range of neurons in hidden layer</strong>
                            <span class="value">start: {value.start}, stop: {value.stop}, step: {value.step}</span>
                        {:else if key === 'file_path'}
                            <strong>Path to results</strong>
                            <span class="value">{value}</span>
                        {:else if key === 'eve'}
                            <strong>Selected number of Eve machines</strong>
                            <span class="value">{value}</span>
                        {:else}
                            <strong>{key}</strong>
                            <span class="value">{value}</span>
                        {/if}
                    </div>
                </div>
            {/each}

            {#if ['running', 'cancelled', 'finished', 'stopping'].includes(simulationData.status) && simulationData.parameters?.file_path}
                <div class="result-file">
                    <p>View the current results:</p>
                    <a href={`http://127.0.0.1:8000/simulator/download/${task_id}`} target="_blank" rel="noopener noreferrer">
                        Download Result CSV
                    </a>
                </div>
            {/if}
        {:else if (task_id == null)}
            <pre>No simulation found with this ID: {task_id}</pre>
        {:else}
            <p>Loading simulation data...</p>
        {/if}
    </div>
</div>

