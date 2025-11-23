<script lang="ts">
    import Habit from '../lib/Habit.svelte';
    import AddHabitDialog from '../lib/addHabitDialog.svelte';
    import type { habit } from '../lib/types/types.ts';
    import { habitsStore } from '../lib/stores/habitsStore';
    import { userStore } from '../lib/stores/userStore';
    import { onMount } from "svelte";

    let show = $state(false);

    onMount(async () => {
        // Only fetch habits if user is logged in
        if ($userStore) {
            await habitsStore.fetchHabits();
        }
        console.log($habitsStore.habits);});

    async function handleHabitAdded() {
        // Refresh habits after adding a new one
        await habitsStore.fetchHabits();
        show = false;
    }
</script>

<div class="bg-stone-950 h-full w-full flex flex-col items-start p-4 space-y-4 relative overflow-y-clip">
    <!--  Header  -->
    <header class="w-full grid grid-cols-2 grid-rows-2 gap-2">
        <h1 class="text-4xl font-bold text-white col-start-1 row-start-1">
            {#if $userStore}
                Welcome back, {$userStore.username}!
            {:else}
                Welcome to Habit-Tracker!
            {/if}
        </h1>

        <div class="text-right col-start-2 row-start-1">
            {#if $userStore}
                <button
                        class="text-6xl font-bold text-white hover:text-red-500 transition-colors cursor-pointer leading-none"
                        onclick={() => show = !show}
                        title="Add new habit"
                >
                    +
                </button>
            {/if}
        </div>

        <div class="col-start-1 row-start-2">
            {#if !$userStore}
                <p class="text-lg text-gray-300">
                    Please login to start tracking your habits!
                </p>
            {:else if $habitsStore.loading}
                <p class="text-lg text-gray-300">
                    Loading your habits...
                </p>
            {:else if $habitsStore.error}
                <p class="text-lg text-red-400">
                    Error loading habits: {$habitsStore.error}
                </p>
            {:else if $habitsStore.habits.length === 0}
                <p class="text-lg text-gray-300">
                    For now there is nothing here.<br>
                    You can add a habit by clicking + in the right top corner!
                </p>
            {:else}
                <p class="text-lg text-gray-300">
                    Remember to check off your habits :)
                </p>
            {/if}
        </div>
    </header>

    <section class="h-full w-1/2 flex flex-col">
        {#if $userStore && !$habitsStore.loading}
            {#if $habitsStore.habits.length > 0}
                <div class="w-full lg:w-2/3 h-fit flex flex-col border-2 border-gray-400 rounded-[1.25rem] items-start p-2 gap-2 overflow-auto">
                    {#each $habitsStore.habits as habitOne (habitOne.id)}
                        <Habit Habit={habitOne} />
                    {/each}
                </div>
            {:else if !$habitsStore.error}
                <div class="w-full text-center py-12">
                    <p class="text-xl text-gray-500 mb-4">No habits yet!</p>
                </div>
            {/if}
        {:else if !$userStore}
            <div class="w-full text-center py-12">
                <p class="text-xl text-gray-500">Login to see your habits</p>
            </div>
        {/if}
    </section>
</div>

{#if show}
    <AddHabitDialog onClose={handleHabitAdded}/>
{/if}