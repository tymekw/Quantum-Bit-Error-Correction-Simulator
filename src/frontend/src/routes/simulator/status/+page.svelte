<script>
    import { onMount } from 'svelte';

    let running_simulations = [];
    let all_simulations = [];
    let error = null;

    const fetchData = async () => {
        try {
            const response = await fetch('http://127.0.0.1:8000/simulator/running-simulations');
            const data = await response.json();
            running_simulations = data['simulations'];
        } catch (err) {
            error = err.message;
        }

        try {
            const response = await fetch('http://127.0.0.1:8000/simulator/all-simulations');
            const data = await response.json();
            all_simulations = data['simulations'];
        } catch (err) {
            error = err.message;
        }
    };

    onMount(() => {
        fetchData();
        const interval = setInterval(fetchData, 10000);
        return () => clearInterval(interval);
    });

    // Helper function to check if a simulation is running
    const isRunning = (simulation) => running_simulations.includes(simulation);
</script>

<style>
    .simulation-list {
        list-style: none;
        padding: 0;
    }

    .simulation-item {
        margin: 10px 0;
        padding: 10px;
        border-radius: 5px;
        background-color: #f8f9fa;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .simulation-item.running {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
    }

    .status-badge {
        font-size: 0.8rem;
        color: white;
        background-color: #28a745;
        padding: 5px 10px;
        border-radius: 3px;
    }
</style>

<div class="container-fluid">
    <div class="col-md-8">
        <h1>Simulations:</h1>

        {#if error}
            <p>Error: {error}</p>
        {:else}
            <ul class="simulation-list">
                {#each all_simulations as simulation}
                    <li class="simulation-item {isRunning(simulation) ? 'running' : ''}">
                        <a href="/simulator/status/{simulation}">Simulation {simulation}</a>
                        {#if isRunning(simulation)}
                            <span class="status-badge">Running</span>
                        {/if}
                    </li>
                {/each}
            </ul>
        {/if}
    </div>
</div>
