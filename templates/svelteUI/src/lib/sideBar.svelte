<script lang="ts">
    import { page } from '$app/stores';
    import LoginDialog from './loginDialog.svelte';
    import { userStore } from './stores/userStore';

    let { side } = $props();

    let isOpen = $state(false);
    let show = $state(false);

    const links = [
        { name: 'Home', href: '/' },
        // { name: 'Statistics', href: '/statistics' },
        { name: 'Settings', href: '/settings' }
    ];

    async function handleLogout() {
        try {
            await fetch('http://localhost:8000/logout', {
                credentials: 'include'
            });
            userStore.logout();
        } catch (err) {
            console.error('Logout failed:', err);
        }
    }
</script>

<div class="h-screen bg-black border-solid text-white {isOpen ? 'w-48' : 'w-16'} flex flex-col p-4 rounded-xl gap-1 transition-all  duration-500 ease-in-out "
>
    <label class="flex mb-4 cursor-pointer"
    class:justify-end={side === 'right'}
    class:justify-left={side  === 'left'}
    >
        <input type="checkbox" class="hidden" onclick={() => isOpen = !isOpen}/>
        <h3 class="transition-all border-2 border-gray-300 rounded-lg size-8 text-center hover:bg-gray-700">
            {#if side === 'left'}
                {isOpen ? '<' : '>' }
            {:else}
                {isOpen ? '>' : '<' }
            {/if}
        </h3>
    </label>

    {#if isOpen}
        {#each links as { name, href }}
            <a
                    class="flex w-11/12 items-center gap-2 p-2 rounded hover:bg-gray-700 text-center transition-all duration-300"
                    class:bg-red-800={$page.url.pathname === href}
                    class:hover:bg-red-650={$page.url.pathname === href}
                    class:font-bold={$page.url.pathname === href}
                    href={href}
            >
                <span>{name}</span>
            </a>
        {/each}
        <div class="mt-auto w-full flex flex-col gap-2 justify-center">
            {#if $userStore}
                <!-- Logged in - show username and logout -->
                <div class="p-2 w-11/12 mx-auto rounded-xl bg-gray-800 border-2 border-gray-600 text-center">
                    <p class="text-sm text-gray-300 truncate">{$userStore.username}</p>
                </div>
                <button
                        class="p-2 w-11/12 mx-auto rounded-xl bg-red-600 hover:bg-red-700 transition-all duration-300
                           border-2 border-red-500 hover:border-red-400 cursor-pointer"
                        onclick={handleLogout}
                >
                    Logout
                </button>
            {:else}
                <!-- Not logged in - show login button -->
                <button
                        class="p-2 w-11/12 mx-auto rounded-xl bg-gray-950/90 hover:bg-gray-100/10 transition-all duration-300
                           border-2 border-gray-300/75 hover:border-gray-300 cursor-pointer"
                        onclick={() => show = true}
                >
                    Login
                </button>
            {/if}
        </div>
    {/if}
</div>

{#if show}
    <LoginDialog type="login" onClose={() => show = false}/>
{/if}
