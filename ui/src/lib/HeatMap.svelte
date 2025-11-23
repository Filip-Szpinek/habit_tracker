<script lang="ts">
    import type { logDate } from './types/types.ts';
    import type { habit } from "./types/types.ts";

    let {Habit} : { Habit: habit} = $props();

    const amount: number = Habit.amount;
    const logs: logDate[] = Habit.logs;
    const firstday = new Date(logs[logs.length - 1].date).getDay();


    function calculating(): { date: string; perday: number }[] {
        if (!logs || logs.length === 0) return [];

        // Sort logs newest → oldest (your data is already this way)
        const sorted = [...logs].sort(
            (a, b) => new Date(a.date).valueOf() - new Date(b.date).valueOf()
        );

        const firstDate = new Date(sorted[0].date);                  // earliest (e.g. 2025-11-15)
        const lastDate = new Date(sorted[sorted.length - 1].date);    // latest  (e.g. 2025-11-23)

        const result: { date: string; perday: number }[] = [];

        // Walk from first day → last day
        const cursor = new Date(firstDate);

        while (cursor <= lastDate) {
            const iso = cursor.toISOString().slice(0, 10);

            // find matching entry for this exact day
            const logEntry = sorted.find(l =>
                new Date(l.date).toISOString().slice(0, 10) === iso
            );

            let perday = 0;

            if (logEntry) {
                perday = logEntry.logs.filter(l => l.completed).length;
            }

            result.push({
                date: iso,
                perday
            });

            // next day
            cursor.setDate(cursor.getDate() + 1);
        }

        return result;
    }

    const bydate = calculating();
</script>

<div class="w-2/3 h-fit mb-4 grid grid-rows-7 grid-flow-col auto-cols-min gap-1 rounded-br-2xl border-b-2 border-r-2 bg-gray-800 border-gray-600 p-2">
    {#each {length: (firstday + 6) % 7} as empty}
        <div class="size-6 bg-transparent"></div>
    {/each}
    {#each bydate as log}
            <div class="size-6 rounded-sm bg-green-600"
                 style="opacity: {Math.max(0, Math.min(1, (log.perday || 0) / (amount || 1)))}"
                 title="{log.date} :  {amount} : {log.perday} "
            >
            </div>
    {/each}
</div>