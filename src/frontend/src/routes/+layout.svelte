<script>
    let { children } = $props()
</script>

<nav>
    <a href="/">Home</a>
    <a href="/simulator">Simulator</a>
    <a href="/simulator/status">Currently running simulations</a>
</nav>

{@render children()}
