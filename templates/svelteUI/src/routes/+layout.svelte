<script lang="ts">
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';
	import SideBar from '$lib/sideBar.svelte';
    import { onMount } from 'svelte';

    let side = $state('right');

    onMount(() => {
        if (!localStorage.getItem('side')) {
            localStorage.setItem('side', 'right');
        } else {
            side = localStorage.getItem('side') as string;
        }
    });

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
    <title>Habit Tracker</title>
</svelte:head>

<main class="flex h-screen bg-[#111]">
    {#if side === 'left'}
        <SideBar {side} />
    {/if}
    <div class="flex-1 overflow-y-auto text-[#eee]">
        {@render children()}
    </div>
    {#if side === 'right'}
        <SideBar {side} />
    {/if}
</main>