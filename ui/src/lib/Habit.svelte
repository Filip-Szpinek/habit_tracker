<script lang="ts">
    import type { habit } from '$lib/types/types.ts';

    const {Habit}: {Habit: habit} = $props();

    const { title, description, frequency, amount, logs} = Habit;
</script>

<section class="max-h-46 min-h-30 w-full mb-4">
    <div class="flex flex-col relative text-white w-full">
        <div class="w-[80%] min-h-30 bg-gray-600 rounded-lg p-4">
            <h2 class="text-2xl font-bold mb-2">{title}</h2>
            {#if description}
                <p class="mb-2">{description}</p>
            {/if}
            <p class="mb-2">Frequency: <span class="italic">{frequency}</span></p>
        </div>
        <div class="absolute w-[33%] h-full rounded-lg top-0 right-0 bg-gray-800 overflow-y-scroll overflow-x-clip">
            <ol class="list-disc list-inside">
                {#each logs as datelog, index}
                    {@const currentDate = new Date(datelog.date)}
                    {@const cols = amount > 4 ? Math.round(amount/2) : amount}

                    {#if currentDate.getMonth() !== (index > 0 ? new Date(logs[index - 1].date).getMonth() : -1)}
                        <div class="font-semibold text-left pl-8 w-full sticky top-0 bg-gray-800 z-10">
                            <span>{currentDate.toLocaleString('pl-PL', {month: 'long'})}</span>
                            <span>{currentDate.getFullYear()}</span>
                        </div>
                    {/if}
                    <li type="none">
                        <span class="top-0 left-1 z-10 sticky">{currentDate.getDate()}</span>
                        <div class="relative size-full grid grid-flow-col border-2 border-gray-200"
                             class:grid-rows-1={amount === 1}
                             class:grid-rows-2={amount > 1}
                        >
                            {#each datelog.logs as log}
                                <div class="h-6 w-full text-center text-sm" class:bg-green-700={log.completed}>{log.time}</div>
                            {/each}
                        </div>
                    </li>
                {/each}
            </ol>
        </div>
    </div>
</section>