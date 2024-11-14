<script>
    let { children } = $props()
</script>
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
<nav class="navbar navbar-expand-lg navbar-light bg-light">
 <div class="collapse navbar-collapse" id="navbarNav">
     <ul class="navbar-nav">
        <li class="nav-item active">
            <a class="nav-link" href="/">Home</a>
        </li>
        <li class="nav-item active">
            <a class="nav-link" href="/simulator">Simulator</a>
        </li>
        <li class="nav-item active">
            <a class="nav-link" href="/simulator/status">Currently running simulations</a>
        </li>
     </ul>
 </div>
</nav>
{@render children()}
