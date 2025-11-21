<script lang="ts">
    import Router from 'svelte-spa-router';
    import './app.css';
    import favicon from './lib/assets/favicon.svg';
    import Sidebar from './lib/sideBar.svelte';
    import { onMount } from 'svelte';

    let side = $state('right');

    onMount(() => {
        if (!localStorage.getItem('side')) {
            localStorage.setItem('side', 'right');
        } else {
            side = localStorage.getItem('side') as string;
        }
    });

    import Home from './routes/Home.svelte';
    import Settings from './routes/Settings.svelte';

    const routes = {
        '/': Home,
        '/settings': Settings
    };
</script>

<svelte:head>
    <link rel="icon" href={favicon} />
    <title>Habit Tracker</title>
</svelte:head>

<div  class="flex h-screen bg-[#111]">
    {#if side === 'left'}
        <Sidebar {side} />
    {/if}
    <main class="flex-1 overflow-y-auto text-[#eee]">
        <!-- SPA router -->
        <Router {routes} />
    </main>
    {#if side === 'right'}
        <Sidebar {side} />
    {/if}
</div>

