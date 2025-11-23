<script lang="ts">
    import Router from 'svelte-spa-router';
    import './app.css';
    import { sideStore } from './lib/stores/sidebarStore'
    import { userStore } from './lib/stores/userStore';
    import { habitsStore } from './lib/stores/habitsStore';
    import { onMount } from 'svelte';
    import favicon from './lib/assets/favicon.svg';
    import Sidebar from './lib/sideBar.svelte';

    import Home from './routes/Home.svelte';
    import Settings from './routes/Settings.svelte';

    let position = $state('right');

    onMount(() => {
        // Load sidebar position
        const storedSide = localStorage.getItem('side');
        if (storedSide) {
            position = storedSide;
            sideStore.setSide(storedSide);
        } else {
            sideStore.setSide(position);
        }

        // If user is logged in (from localStorage), fetch their habits
        if ($userStore) {
            habitsStore.fetchHabits();
        }
    });

    const routes = {
        '/': Home,
        '/settings': Settings
    };
</script>

<svelte:head>
    <link rel="icon" href={favicon} />
    <title>Habit Tracker</title>
</svelte:head>

<div class="flex h-screen bg-[#111]">
    {#if position === 'left'}
        <Sidebar {position} />
    {/if}
    <main class="flex-1 overflow-y-auto text-[#eee]">
        <Router {routes} />
    </main>
    {#if position === 'right'}
        <Sidebar {position} />
    {/if}
</div>