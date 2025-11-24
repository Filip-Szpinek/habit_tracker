<script lang="ts">
    import { location, push } from 'svelte-spa-router';
    import LoginDialog from './loginDialog.svelte';
    import { userStore } from './stores/userStore';
    import { habitsStore } from './stores/habitsStore';

    let { position } = $props();

    let isOpen = $state(false);
    let show = $state(false);

    const links = [
        { name: 'Home', href: '/' },
        { name: 'Settings', href: '/settings' }
    ];

    async function handleLogout() {
        try {
            await fetch('/logout', {  // Changed from http://localhost:8000/logout
                credentials: 'include'
            });
            userStore.logout();
            habitsStore.clear();
            push('/');
        } catch (err) {
            console.error('Logout failed:', err);
        }
    }

    function isActive(href: string) {
        return $location === href;
    }
</script>

<div class="h-screen bg-black border-solid text-white {isOpen ? 'w-48' : 'w-16'} flex flex-col p-4 rounded-xl gap-1 transition-all duration-500 ease-in-out">
    <label class="flex mb-4 cursor-pointer"
           class:justify-end={position === 'right'}
           class:justify-start={position === 'left'}
    >
        <input type="checkbox" class="hidden" onclick={() => isOpen = !isOpen}/>
        <h3 class="transition-all border-2 border-gray-300 rounded-lg size-8 text-center hover:bg-gray-700 flex items-center justify-center cursor-pointer">
            {#if position === 'left'}
                {isOpen ? '<' : '>' }
            {:else}
                {isOpen ? '>' : '<' }
            {/if}
        </h3>
    </label>

    {#if isOpen}
        {#each links as { name, href }}
            <button
                    class="flex w-11/12 items-center gap-2 p-2 rounded hover:bg-gray-700 text-left transition-all duration-300"
                    class:bg-red-800={isActive(href)}
                    class:hover:bg-red-650={isActive(href)}
                    class:font-bold={isActive(href)}
                    onclick={() => push(href)}
            >
                <span>{name}</span>
            </button>
        {/each}

        <div class="mt-auto w-full flex flex-col gap-2 justify-center">
            {#if $userStore}
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
                <button
                        class="p-2 w-11/12 mx-auto rounded-xl bg-gray-950/90 hover:bg-gray-100/10 transition-all duration-300
                           border-2 border-gray-300/75 hover:border-gray-300 cursor-pointer"
                        onclick={() => show = true}
                >
                    Login
                </button>
            {/if}
        </div>
    {:else}
        <!-- Collapsed view - show user initial or login icon -->
        <div class="mt-auto w-full flex justify-center">
            {#if $userStore}
                <div class="size-8 rounded-full bg-red-600 flex items-center justify-center font-bold text-sm cursor-default" title={$userStore.username}>
                    {$userStore.username.charAt(0).toUpperCase()}
                </div>
            {:else}
                <button
                        class="size-8 rounded-lg bg-gray-700 hover:bg-gray-600 flex items-center justify-center transition-all cursor-pointer"
                        onclick={() => show = true}
                        title="Login"
                >
                    👤
                </button>
            {/if}
        </div>
    {/if}
</div>

{#if show}
    <LoginDialog type="login" onClose={() => show = false}/>
{/if}