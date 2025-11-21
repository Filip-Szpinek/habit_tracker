<script lang="ts">
    let { onClose } = $props();

    let name = $state('');
    let description = $state('');
    let frequency = $state('');

    let error = $state('');
    let loading = $state(false);
    let successMessage = $state('');

    async function postHabit() {
        loading = true;
        error = '';
        successMessage = '';

        try {
            const formData = new FormData();
            formData.append('login', name);
            formData.append('password', description);
            formData.append('password', frequency);

            const response = await fetch('http://localhost:8000/add-habit', {
                method: 'POST',
                credentials: 'include',
                body: formData
            });

            if (!response.ok) {
                const data = await response.json();
                error = data.detail || 'adding failed';
                return;
            }

            const data = await response.json();
            console.log('added habit successfully:', data);

            successMessage = 'added habit successful!';

            setTimeout(() => {onClose?.();}, 1000);

        } catch (err) {
            console.error('Error:', err);
            error = 'Connection error.';
        } finally {
            loading = false;
        }
    }

</script>

<div
        class="fixed inset-0 bg-black/50 z-40"
        onclick={() => onClose?.()}
></div>

<section class="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-50 w-full max-w-md px-4 scale-120">
    <div class="h-fit text-left bg-white dark:bg-gray-900 rounded-xl shadow-2xl text-white">
        {#if error}
            <div class="mx-8 mt-4 p-3 bg-red-500/20 border-2 border-red-500 rounded-lg text-sm">
                {error}
            </div>
        {/if}

        {#if successMessage}
            <div class="mx-8 mt-4 p-3 bg-green-500/20 border-2 border-green-500 rounded-lg text-sm">
                {successMessage}
            </div>
        {/if}

            <div class="px-8 py-6 mt-4">
                <div class="flex flex-col justify-center items-center h-full select-none">
                    <div class="w-full flex flex-col gap-2">
                        <label class="font-semibold border border-transparent " title="title of a habit">
                            <input
                                bind:value={name}
                                placeholder="Title"
                                class="border-b-1 px-1 py-2 mb-5 text-lg w-full outline-none text-shadow-white dark:bg-gray-900 transition-all duration-75 focus:border-b-2"
                                required
                            />
                        </label>
                    </div>
                    <div class="w-full flex flex-col gap-2">
                        <label class="font-semibold text-xs text-gray-100">Description</label>
                        <input
                                bind:value={description}
                                placeholder="Description"
                                class="border-2 rounded-lg px-3 py-2 mb-5 text-sm w-full outline-none dark:border-gray-500 dark:bg-gray-900"
                                type="text"
                                title="Description"
                                required
                                onkeydown={(e) => e.key === 'Enter' && postHabit()}
                        />
                    </div>
                    <div class="w-full flex flex-col gap-2">
                        <label class="font-semibold text-xs text-gray-100" title="Frequency">Frequency</label>
                        <select
                                bind:value={frequency}
                                class="border-2 rounded-lg px-3 py-2 mb-5 text-sm w-full outline-none dark:border-gray-500 dark:bg-gray-900"
                                required
                        >
                            <option value="daily">Daily</option>
                            <option value="weekly">Weekly</option>
                            <option value="monthly">Monthly</option>
                        </select>
                    </div>
                    <div class="w-full flex flex-row gap-2">
                        <button
                                class="py-2 px-8 bg-gray-600 hover:bg-gray-800 focus:ring-offset-gray-200 text-white w-full
                            transition ease-in duration-200 text-center text-base font-semibold shadow-md focus:outline-none
                            focus:ring-2 focus:ring-offset-2 rounded-lg cursor-pointer select-none disabled:opacity-50"
                                onclick={() => onClose?.()}
                        >
                            Cancel
                        </button>
                        <button
                                class="py-2 px-8 bg-red-600 hover:bg-red-800 focus:ring-offset-red-200 text-white w-full
                            transition ease-in duration-200 text-center text-base font-semibold shadow-md focus:outline-none
                            focus:ring-2 focus:ring-offset-2 rounded-lg cursor-pointer select-none disabled:opacity-50"
                                onclick={() => postHabit()}
                                disabled={loading}
                        >
                            {loading ? 'adding...' : 'Add'}
                        </button>
                    </div>
                </div>
            </div>
        </div>
</section>