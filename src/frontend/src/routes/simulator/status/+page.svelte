<script>
    import { onMount } from 'svelte';

    let simulations = [];
    let error = null;
    const fetchData = async () => {
        try {
            const response = await fetch('http://127.0.0.1:8000/simulator/running-simulations');
            const data = await response.json();
            simulations = data['running simulations'];
        } catch (err) {
            error = err.message;
        }
    };

    onMount(() => {
        // Initial data fetch
        fetchData();
        // Set interval to fetch data every 10 seconds (10000 ms)
        const interval = setInterval(fetchData, 10000);
        // Clean up the interval when the component is destroyed
        return () => clearInterval(interval);
    });
</script>

<h1>Currently running simulations:</h1>

{#if error}
    <p>Error: {error}</p>
{:else}
    <ul>
        {#each simulations as item}
            <li><a href="/simulator/status/{item}">Simulation {item}</a></li>
        {/each}
    </ul>
{/if}
