<script lang="ts">
    import { onMount } from 'svelte';

    let side = $state('left');

    onMount(() => {
        if (!localStorage.getItem('side')) {
            localStorage.setItem('side', 'left');
        } else {
            side = localStorage.getItem('side') as string;
        }
    });

    function onChangeSidebar(setside: string) {
        localStorage.setItem('side', setside);
        side = setside;
    }
</script>

<main>
    <div class="flex flex-col items-center justify-center h-full text-white">
        <h1 class="text-4xl font-bold mb-6">Settings</h1>
    </div>

    <section class="flex flex-col gap-4 border border-white rounded-lg p-6 mb-6 bg-gray-950/50">
        <h2 class="text-2xl font-semibold mb-4">Preferences</h2>

        <div class="flex flex-row">
            <span>Sidebar</span>
            <div class="flex flex-row gap-2 rounded-4 border-2 border-gray-300 w-fit rounded-lg">
                <label class="rounded-md cursor-pointer">
                    <input type="radio" name="sidebar" value="left"  onclick={() => onChangeSidebar('left')} checked={side === 'left'} />
                    <span class="pl-4 pr-4 pt-2 pb-2 rounded-md font-semibold border-2 transition-all border-transparent hover:border-amber-50">
						Left
					</span>
                </label>
                <label class="rounded-md cursor-pointer">
                    <input type="radio"
                           name="sidebar"
                           value="right"
                           onclick={() => onChangeSidebar('right')}
                           checked={side === 'right'}/>
                    <span class="pl-4 pr-4 pt-2 pb-2 rounded-md font-semibold border-2 transition-all border-transparent hover:border-amber-50">
						Right
					</span>
                </label>
            </div>
        </div>

    </section>

</main>

<style>
    input[type="text"], input[type="password"] {
        margin-left: 1rem;
        padding: 0.5rem;
        border-radius: 0.375rem;
        border: 1px solid #ccc;
        background-color: #1f2937; /* Tailwind's gray-800 */
        color: white;
    }

    label {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
    }

    input[type="radio"] {
        margin-left: 0.5rem;
        width: 1rem;
        height: 1rem;
        accent-color: #ef4444; /* Tailwind's red-500 */
        display: none;
    }

    label > input[type="radio"]:checked + span{
        background-color: #ef4444;
    }

    input:disabled{
        background-color: transparent;
        color: #9ca3af; /* Tailwind's gray-400 */
    }

</style>

