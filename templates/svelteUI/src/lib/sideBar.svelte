<script lang="ts">
    import { page } from '$app/stores';
    import LoginDialog from './loginDialog.svelte'

    let { side } = $props();

    let isOpen = $state(false);
    let show = $state(false);

    const links = [
        { name: 'Home', href: '/' },
        { name: 'Settings', href: '/settings' }
    ];
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
        <div class="mt-auto w-full flex justify-center">
            <button class="mt-auto p-2 w-11/12 rounded-xl bg-gary-950/90 hover:bg-gray-100/10 transition-all duration-300
                            border-2 border-gray-300/75 hover:border-gray-300  cursor-pointer"
                    onclick={() => show = true}
            >
                Login
            </button>
        </div>
    {/if}
</div>

{#if show}
    <LoginDialog type="login" onClose={() => show = false}/>
{/if}
