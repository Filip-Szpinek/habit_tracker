<script lang="ts">
    import Habit from '../lib/Habit.svelte';
    import AddHabitDialog from '../lib/addHabitDialog.svelte';
    import type { habit } from '../lib/types/types.ts';
    import {onMount} from "svelte";

    let date = new Date();
    let listHabits = $state([] as habit[]);

    let show = $state(false);

    let habitLoading: habit = {
        id: 0,
        title: 'Loading...',
        description: 'Please wait while we load your habits.',
        frequency: 'daily',
        amount: 1,
        startDate: (date.setDate(date.getDate() - 5), date.toISOString()),
        logs: [
            { date: (date.setDate(date.getDate() + 5), date.toISOString()),
                logs: [
                    {time: '08:00',count: 1, completed: true}
                ] },
            { date: (date.setDate(date.getDate() - 1), date.toISOString()),
                logs: [
                    {time: '07:00',count: 1, completed: true}
                ] },
            { date: (date.setDate(date.getDate() - 1), date.toISOString()),
                logs: [
                    {time: '15:00',count: 1, completed: true}
                ] },
            { date: (date.setDate(date.getDate() - 1), date.toISOString()),
                logs: [
                    {time: '06:00',count: 1, completed: true}
                ] },
            { date: (date.setDate(date.getDate() - 1), date.toISOString()),
                logs: [
                    {time: '18:00',count: 1, completed: true}
                ] },
        ]
    };

    listHabits.push(habitLoading)

    onMount(async () => {
        const res = await fetch('/exampleHabits.json');
        listHabits = [];
        listHabits = await res.json();
    });

</script>

<div class="bg-stone-950 h-full w-full flex flex-col items-start p-4 space-y-4 relative">
    <!--  Add button  -->
    <header class="w-full grid grid-cols-2 grid-rows-1">
        <div class="text-right col-2 row-end-1 cursor-pointer">
            <button class="text-6xl font-bold text-white h-0 text-right cursor-pointer"
                    onclick={() => show = !show}>+</button>
        </div>
        <h1 class="text-4xl font-bold text-white col-start-1 row-end-1">Welcome to Habit-Tracker!</h1>
        {#if listHabits === null || listHabits.length === 0}
            <p class="text-lg text-gray-300 text-left col-start-1 row-start-1">
                For now there is nothing here.<br> You can add a habit by clicking + in the right top corner!
            </p>
        {:else}
            <p class="text-lg text-gray-300 text-left col-start-1 row-start-1">
                Remember to check of your habits :)
            </p>
        {/if}

    </header>

    <section class="h-full w-full flex flex-col">
        <div class="w-1/3 h-fit flex flex-col border-2 border-gray-400 rounded-[1.25rem] items-start p-2">
            {#each listHabits as habitOne}
                <Habit Habit={habitOne} />
            {/each}
        </div>
    </section>
</div>

{#if show}
    <AddHabitDialog onClose={() => show = false}/>
{/if}