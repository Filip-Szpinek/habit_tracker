<script lang="ts">
    import type { habit } from './types/types.ts';
    import { habitsStore } from './stores/habitsStore';
    const {Habit}: {Habit: habit} = $props();

    const { title, description, frequency, logs} = Habit;

    let deleting = $state(false);
    let toggling = $state(false);

    async function handleDelete() {
        if (!confirm(`Are you sure you want to delete "${Habit.title}"?`)) {
            return;
        }

        deleting = true;
        await habitsStore.deleteHabit(Habit.id);
        deleting = false;
    }

    async function handleToggle() {
        toggling = true;
        await habitsStore.toggleHabit(Habit.id);
        toggling = false;
    }
</script>

<section class="max-h-46 min-h-30 w-full mb-4">
    <div class="flex flex-col relative text-white w-full peer">
        <button
                onclick={handleDelete}
                class="flex absolute top-1 left-1 p-1 bg-red-600/80 hover:bg-red-700 rounded-md text-xs disabled:opacity-50 peer-hover:flex"
                title="Delete habit"
                disabled={deleting}
        >
            {deleting ? '...' : '✕'}
        </button>
        <div class="w-[80%] min-h-30 bg-gray-600 rounded-lg p-4">
            <h2 class="text-2xl font-bold mb-2">{title}</h2>
            {#if description}
                <p class="mb-2">{description}</p>
            {/if}
            <p class="mb-2">Frequency: <span class="italic">{frequency}</span></p>
        </div>
<!--        <button-->
<!--                onclick={handleToggle}-->
<!--                class="w-full px-4 py-2 bg-green-600 hover:bg-green-700 rounded-lg transition-colors disabled:opacity-50"-->
<!--                disabled={toggling}-->
<!--        >-->
<!--            {toggling ? 'Updating...' : 'Mark as Done Today'}-->
<!--        </button>-->
        <div class="absolute w-[33%] h-full rounded-lg top-0 right-0 bg-gray-800 overflow-y-scroll overflow-x-clip">
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