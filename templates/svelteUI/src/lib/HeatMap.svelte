<script lang="ts">
    import type { habitLog } from '$lib/types/types.ts';
    import KafelekHeatMap from "$lib/KafelekHeatMap.svelte";

    export let amount: number;
    export let logs: habitLog[];
</script>

<div class="w-full h-full grid grid-cols-7 gap-1">
    {#each logs as log (log.date)}
        <KafelekHeatMap date={log.date} amount={amount} completed={log.completed} />
    {/each}
</div>