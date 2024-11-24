<script>
    import { onMount } from 'svelte';

    export let data;  // Initial data passed from load function
    export let error;

    let simulationData = data?.data || null;  // Initialize simulation data
    let task_id = simulationData?.task_id;   // Extract task_id from initial data

    // Function to fetch new data from the API
    const fetchData = async () => {

        if (task_id == null || simulationData.status !== 'running') return; // If no task_id, don't send the request
        try {
            const response = await fetch(`http://127.0.0.1:8000/simulator/status/${task_id}`);
            if (!response.ok) throw new Error('Failed to fetch data');
            simulationData = await response.json();
            task_id = simulationData.task_id
            error = null; // Reset any previous error
        } catch (err) {
            error = err.message; // Set error message if fetch fails
            console.error("Fetch error:", err);
        }
    };

    // Function to cancel the task by sending a POST request
    const cancelTask = async () => {
        if (task_id == null || simulationData.status !== 'running') return; // If no task_id, don't send the request
        try {
            const response = await fetch(`http://127.0.0.1:8000/simulator/cancel-simulation/${task_id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
            });

            if (!response.ok) throw new Error('Failed to cancel task');
            const result = await response.json();
            await fetchData();
        } catch (err) {
            error = err.message; // Set error message if the request fails
            console.error("Cancel error:", err);
        }
    };

    onMount(() => {
        // Initial fetch when the component is mounted
        fetchData();
        // Set interval to fetch data every 10 seconds (10000 ms)
        const interval = setInterval(fetchData, 10000);
        // Clean up the interval when the component is destroyed
        return () => clearInterval(interval);
    });
</script>

<style>
    .status {
        display: flex;
        align-items: center;
        gap: 10px;
        font-weight: bold;
    }

    .status.not_started { color: gray; }
    .status.started { color: blue; }
    .status.running { color: green; }
    .status.stopping { color: orange; }
    .status.cancelled { color: red; }
    .status.finished { color: darkgreen; }

    .spinner {
        border: 4px solid rgba(0, 255, 0, 0.3); /* Light green border */
        border-top: 4px solid green; /* Solid green top */
        border-radius: 50%;
        width: 20px;
        height: 20px;
        animation: spin 1s linear infinite;
        display: inline-block;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>


<div class="container-fluid">
    <div class="col-md-8">
        {#if error}
            <p>Error: {error}</p>
        {:else if (simulationData && task_id != null)}
            <h1>Status of simulation with id: {task_id}</h1>

            <!-- Main status div with status message and cancel button -->
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

                <!-- Display Cancel button only if running -->
                {#if simulationData.status === 'running'}
                    <button class="btn btn-primary" on:click={cancelTask}>Cancel Task</button>
                {/if}
            </div>

            <!-- Separate div for result file link, displayed below the main status -->
            {#if ['running', 'cancelled', 'finished', 'stopping'].includes(simulationData.status) && simulationData.parameters?.file_path}
                <div class="result-file mt-3">
                    <p>View current results:</p>
                    <a href={`http://127.0.0.1:8000/simulator/download/${task_id}`} target="_blank" rel="noopener noreferrer" class="btn btn-secondary">
                        Download Result CSV
                    </a>
                </div>
            {/if}

        {:else if (task_id == null)}
            <pre>No simulation with this id: {task_id}!</pre>
        {:else}
            <p>Loading simulation data...</p>
        {/if}
    </div>
</div>
