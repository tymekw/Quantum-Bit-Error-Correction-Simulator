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

<h1>Currently running simulation data for Task ID: {task_id}</h1>

{#if error}
    <p>Error: {error}</p>
{:else if (simulationData && task_id != null)}
    <pre>{JSON.stringify(simulationData, null, 2)}</pre>
    {#if (simulationData.status === 'running') }
         <button class="btn btn-primary" on:click={cancelTask}>Cancel Task</button>
    {/if}
{:else if (task_id == null)}
    <pre>No simulation with this id: {task_id}!</pre>
{:else}
    <p>Loading simulation data...</p>
{/if}
