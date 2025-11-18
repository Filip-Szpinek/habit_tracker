<script lang="ts">
    import Habit from '$lib/Habit.svelte';
    import type { habit } from '$lib/types/types.ts';
    import {onMount} from "svelte";

    let date = new Date();
    let listHabits = $state([] as habit[]);

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

<div class="bg-stone-950 h-full w-full flex flex-col items-start p-4 space-y-4">
    <h1 class="text-4xl font-bold text-white">Welcome to Habit-Tracker!</h1>
    <p class="text-lg text-gray-300 text-center">
        For now there is nothing here, but stay tuned for updates!
    </p>
    <section class="h-full w-full flex flex-col">
        <div class="w-1/3 h-fit flex flex-col border-2 border-gray-400 rounded-[1.25rem] items-start p-2">
            {#each listHabits as habitOne}
                <Habit Habit={habitOne} />
            {/each}
        </div>
    </section>
</div>