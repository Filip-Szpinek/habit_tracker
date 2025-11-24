<script lang="ts">
    import type { Habit } from './types/types.ts';
    import { habitsStore } from './stores/habitsStore';
    const {habit}: {habit: Habit} = $props();

    const { name, description, frequency, logs} = habit;

    let deleting = $state(false);
    let toggling = $state(false);

    async function handleDelete() {
        if (!confirm(`Are you sure you want to delete "${habit.name}"?`)) {
            return;
        }

        deleting = true;
        await habitsStore.deleteHabit(habit.id);
        deleting = false;
    }

    async function handleToggle() {
        toggling = true;
        await habitsStore.toggleHabit(habit.id);
        toggling = false;
    }

    function isSameDay(a: string | Date, b: Date = new Date()) {
        const d = typeof a === 'string' ? new Date(a) : a;
        return d.getFullYear() === b.getFullYear()
            && d.getMonth() === b.getMonth()
            && d.getDate() === b.getDate();
    }

    export function getTodaysLogStatus(habit: Habit): { found: boolean; completed: boolean | null } {
        const today = new Date();

        for (const datelog of habit.logs ?? []) {
            if (datelog.date && isSameDay(datelog.date, today)) {
                const entries = Array.isArray(datelog.logs) ? datelog.logs : [];

                if (entries.length === 0) return { found: true, completed: null };

                const completed = entries.some(l => !!l.completed);
                return { found: true, completed };
            }
        }
        return { found: false, completed: null };
    }

    const todaysLog = getTodaysLogStatus(habit);

</script>

<section class="max-h-46 min-h-30 w-full mb-4">
    <div class="flex flex-col relative text-white w-full h-full overflow-clip">
        <div class="relative w-[70%] min-h-30 bg-gray-600 rounded-lg p-4 group transition-all duration-500 hover:pt-14">
            <div class="absolute h-0 top-0 left-0 w-[90%] hidden transition-all duration-500 group-hover:flex group-hover:h-fit gap-2 p-2 ">
                <button
                        onclick={handleDelete}
                        class="w-1/6 p-1 bg-red-600/80 hover:bg-red-700 rounded-md text-xs disabled:opacity-50"
                        title="Delete habit"
                        disabled={deleting}
                >
                    {deleting ? '...' : 'X'}
                </button>

                <button
                        onclick={handleToggle}
                        class="w-5/6 px-4 py-2 border-2 {todaysLog.completed ? 'bg-green-600 border-transparent' : 'bg-transparent border-gray-100'} hover:bg-green-700 rounded-lg
                        transition-colors disabled:opacity-50"
                        disabled={toggling}
                >
                    {#if todaysLog.completed}
                        {toggling ? 'Updating...' : 'Done'}
                    {:else}
                        {toggling ? 'Updating...' : 'Check'}
                    {/if}
                </button>
            </div>
            <h2 class="text-2xl font-bold mb-2">{name}</h2>
            {#if description}
                <p class="mb-2">{description}</p>
            {/if}
            <p class="mb-2">Frequency: <span class="italic">{frequency}</span></p>
        </div>


        <div class="absolute w-[33%] h-full rounded-r-lg top-0 right-0 bg-gray-800 overflow-y-scroll overflow-x-clip">
            <ol class="list-disc list-inside">
                {#each logs as datelog, index}
                    {@const currentDate = new Date(datelog.date)}
                    {#if currentDate.getMonth() !== (index > 0 ? new Date(logs[index - 1].date).getMonth() : -1)}
                        <div class="font-semibold text-left pl-8 w-full sticky top-0 bg-gray-800 z-10">
                            <span>{currentDate.toLocaleString('pl-PL', {month: 'long'})}</span>
                            <span>{currentDate.getFullYear()}</span>
                        </div>
                    {/if}
                    <li type="none">
                        <span class="top-0 left-1 z-10 sticky">{currentDate.getDate()}</span>
                        <div class="relative size-full grid grid-flow-col grid-rows-1 border-2 border-gray-200">
                            {#each datelog.logs as log}
                                <div class="h-6 w-full text-center text-sm" class:bg-green-700={log.completed}>{log.completed ? '✔️' : 'X'}</div>
                            {/each}
                        </div>
                    </li>
                {/each}
            </ol>
        </div>
    </div>
</section>