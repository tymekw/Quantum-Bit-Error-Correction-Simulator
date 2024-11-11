<script>
    import { onMount } from 'svelte';

    export let data;  // Initial data passed from load function
    export let error;

    let simulationData = data?.data || null;  // Initialize simulation data
    let task_id = simulationData?.task_id;   // Extract task_id from initial data

    // Function to fetch new data from the API
    const fetchData = async () => {

        if (task_id == null ) return; // If no task_id, don't fetch
        try {
            const response = await fetch(`http://127.0.0.1:8000/simulator/status/${task_id}`);
            if (!response.ok) throw new Error('Failed to fetch data');
            simulationData = await response.json();

            error = null; // Reset any previous error
        } catch (err) {
            error = err.message; // Set error message if fetch fails
            console.error("Fetch error:", err);
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
{:else if simulationData}
    <pre>{JSON.stringify(simulationData, null, 2)}</pre>
{:else}
    <p>Loading simulation data...</p>
{/if}
