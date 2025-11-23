<script lang="ts">
    import { onMount } from 'svelte';
    import { userStore } from '../lib/stores/userStore';
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

{#snippet  Input(type, value, is_disabled)}
    <label>
        <input type={type}
               value={value}
               disabled={is_disabled}
               class="bg-transparent disabled:text-gray-400/80 disabled:italic px-2 py-1" />
    </label>
{/snippet}

<main>
    <div class="flex flex-col items-center justify-center h-full text-white">
        <h1 class="text-4xl font-bold mb-6">Settings</h1>
    </div>

    <section class="flex flex-col gap-4 border border-white rounded-lg p-6 mb-6 bg-gray-950/50">
        <h2 class="text-2xl font-semibold mb-4">Account</h2>

        <div class="flex flex-col">
            <span>Username</span>
            <div class="flex flex-row gap-2 rounded-4 border-2 border-gray-300 w-fit rounded-lg">
                {#if $userStore}
                    {@render Input("text", $userStore.username, true)}
                    {:else}
                    <p class="p-3 bg-red-600/90 border-4 border-red-700 rounded-lg font-semibold">Unable to get a account information</p>
                {/if}
            </div>
        </div>

    </section>

    <section class="flex flex-col gap-4 border border-white rounded-lg p-6 mb-6 bg-gray-950/50">
        <h2 class="text-2xl font-semibold mb-4">Preferences</h2>

        <div class="flex flex-col">
            <span>Sidebar</span>
            <div class="flex flex-row gap-2 rounded-4 border-3 border-gray-300 w-fit rounded-lg">
                <label class="rounded-md cursor-pointer l-4 pr-4 pt-2 pb-2">
                    <input type="radio"
                           name="sidebar"
                           value="left"
                           onclick={() => onChangeSidebar('left')}
                           checked={side === 'left'}
                           class="hidden peer"
                    />
                    <span class="pl-4 pr-4 pt-2 pb-2 rounded-md font-semibold border-2 transition-all border-transparent hover:border-amber-50
                                 peer-checked:bg-red-700 ">
						Left
					</span>
                </label>
                <label class="rounded-md cursor-pointer l-4 pt-2 pb-2">
                    <input type="radio"
                           name="sidebar"
                           value="right"
                           onclick={() => onChangeSidebar('right')}
                           checked={side === 'right'}
                           class="hidden peer"
                    />
                    <span class="pl-4 pr-4 pt-2 pb-2 rounded-md font-semibold border-2 transition-all border-transparent hover:border-amber-50
                                 peer-checked:bg-red-700">
						Right
					</span>
                </label>
            </div>
        </div>

    </section>

</main>


