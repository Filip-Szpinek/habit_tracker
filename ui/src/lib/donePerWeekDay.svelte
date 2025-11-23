<script lang="ts">
    import type {habit} from "./types/types";

    let {Habit} : { Habit: habit} = $props();
    const dateLogs = Habit.logs;
    const weekdays = [
        {
            day: 'Monday',
            done: 0
        },
        {
            day: 'Tuesday',
            done:  0
        },
        {
            day: 'Wednesday',
            done: 0
        }
        ,
        {
            day: 'Thursday',
            done: 0
        },
        {
            day: 'Friday',
            done: 0
        },
        {
            day: 'Saturday',
            done: 0
        },
        {
            day: 'Sunday',
            done: 0
        }
    ]

    function calculateWeekdayAverages() {
        weekdays.forEach(day => {
            day.done = 0;
        });

        const counts = [0, 0, 0, 0, 0, 0, 0]; // Total days per weekday

        dateLogs.forEach((datelog) => {
            const date = new Date(datelog.date);
            const dayOfWeek = date.getDay();
            const weekdayIndex = dayOfWeek === 0 ? 6 : dayOfWeek - 1;

            // Check if completed
            const wasCompleted = datelog.logs.some(log => log.completed);

            counts[weekdayIndex]++;
            if (wasCompleted) {
                weekdays[weekdayIndex].done++;
            }
        });

        weekdays.forEach((day, index) => {
            if (counts[index] > 0) {
                day.done = (day.done / counts[index]) * 100;
            }
        });
    }

    calculateWeekdayAverages();
</script>

<div class="w-1/3 h-fit mb-4 grid grid-rows-7 gap-1 rounded-bl-2xl border-b-2 border-l-2 bg-gray-800 border-gray-600 p-2">
    {#each weekdays as weekday}
        <section class="w-full flex justify-between h-fit">
            <div>{weekday.day}</div>
            <div>{weekday.done}%</div>
        </section>
    {/each}
</div>