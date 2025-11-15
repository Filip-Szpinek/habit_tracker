<script lang="ts">
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';
	import SideBar from '$lib/sideBar.svelte';


	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
    <title>Habit Tracker</title>
</svelte:head>

<main class="layout">
    <SideBar />
    <div class="content">
        {@render children()}
    </div>
</main>

<style>
    .layout {
        display: flex;
        height: 100vh;
        background: #111;
    }

    .content {
        flex: 1;
        overflow-y: auto;
        color: #eee;
    }
</style>
