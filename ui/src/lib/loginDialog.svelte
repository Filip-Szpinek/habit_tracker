<script lang="ts">
    import { userStore } from './stores/userStore';
    import { habitsStore } from './stores/habitsStore';

    let { type = $bindable('login'), onClose } = $props();

    let username = $state('');
    let password = $state('');
    let password2 = $state('');
    let error = $state('');
    let loading = $state(false);
    let successMessage = $state('');

    async function handleLogin() {
        loading = true;
        error = '';
        successMessage = '';

        try {
            const formData = new FormData();
            formData.append('login', username);
            formData.append('password', password);

            const response = await fetch('/login', {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Accept': 'application/json'  // Tell server we want JSON
                },
                body: formData
            });

            if (!response.ok) {
                const data = await response.json();
                error = data.detail || 'Login failed';
                return;
            }

            const data = await response.json();
            console.log('Login success:', data);

            userStore.login(username);
            await habitsStore.fetchHabits();

            successMessage = 'Login successful!';

            setTimeout(() => {
                onClose?.();
            }, 1000);

        } catch (err) {
            console.error('Error:', err);
            error = 'Connection error. Make sure the server is running.';
        } finally {
            loading = false;
        }
    }

    async function handleRegister() {
        loading = true;
        error = '';
        successMessage = '';

        try {
            const formData = new FormData();
            formData.append('r_login', username);
            formData.append('r_password', password);
            formData.append('r_password2', password2);

            const response = await fetch('/register', {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Accept': 'application/json'  // Tell server we want JSON
                },
                body: formData
            });

            if (!response.ok) {
                const data = await response.json();
                error = data.detail || 'Registration failed';
                return;
            }

            const data = await response.json();
            console.log('Register success:', data);

            userStore.login(username);
            await habitsStore.fetchHabits();

            successMessage = 'Registration successful! Welcome!';

            setTimeout(() => {
                onClose?.();
            }, 1500);

        } catch (err) {
            console.error('Error:', err);
            error = 'Connection error';
        } finally {
            loading = false;
        }
    }

    function clearForm() {
        username = '';
        password = '';
        password2 = '';
        error = '';
        successMessage = '';
    }

    function switchTab(newType: 'login' | 'register') {
        type = newType;
        clearForm();
    }
</script>

<div
        class="fixed inset-0 bg-black/50 z-40"
        onclick={() => onClose?.()}
></div>

<section class="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-50 w-full max-w-md px-4 scale-120">
    <!-- Toggle buttons -->
    <div class="relative w-full flex flex-row gap-2 p-1 bg-white dark:bg-gray-900 text-white rounded-xl font-semibold">
        <label class="w-1/2 text-center cursor-pointer z-10">
            <input
                    type="radio"
                    name="option"
                    checked={type === 'login'}
                    onchange={() => switchTab('login')}
                    class="peer hidden"
            />
            <span class="block w-full px-3 py-2 rounded-lg transition-colors peer-checked:text-white">
                Login
            </span>
        </label>
        <label class="w-1/2 text-center cursor-pointer z-10">
            <input
                    type="radio"
                    name="option"
                    checked={type === 'register'}
                    onchange={() => switchTab('register')}
                    class="peer hidden"
            />
            <span class="block w-full px-3 py-2 rounded-lg transition-colors peer-checked:text-white">
                Register
            </span>
        </label>
        <div
                class="absolute w-[calc(50%-0.25rem)] h-[calc(100%-0.5rem)] rounded-lg top-1 bg-red-500 transition-all duration-300 ease-in-out"
                style="left: {type === 'login' ? '0.25rem' : 'calc(50% + 0.25rem)'};"
        ></div>
    </div>

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

        {#if type === 'login'}
            <div class="px-8 py-6 mt-4">
                <div class="flex flex-col justify-center items-center h-full select-none">
                    <div class="flex flex-col items-center justify-center gap-2 mb-8">
                        <div class="w-8 h-8 bg-gray-700 rounded-full flex items-center justify-center text-2xl">
                            👤
                        </div>
                        <p class="m-0 text-[16px] font-semibold dark:text-white">
                            Login to your Account
                        </p>
                        <span class="m-0 text-xs max-w-[90%] text-center text-[#8B8E98]">
                            Get started with our app, just start section and enjoy experience.
                        </span>
                    </div>
                    <div class="w-full flex flex-col gap-2">
                        <label class="font-semibold text-xs text-gray-100">Username</label>
                        <input
                                bind:value={username}
                                placeholder="Username"
                                class="border rounded-lg px-3 py-2 mb-5 text-sm w-full outline-none dark:border-gray-500 dark:bg-gray-900"
                                disabled={loading}
                        />
                    </div>
                    <div class="w-full flex flex-col gap-2">
                        <label class="font-semibold text-xs text-gray-100">Password</label>
                        <input
                                bind:value={password}
                                placeholder="••••••••"
                                class="border rounded-lg px-3 py-2 mb-5 text-sm w-full outline-none dark:border-gray-500 dark:bg-gray-900"
                                type="password"
                                onkeydown={(e) => e.key === 'Enter' && !loading && handleLogin()}
                                disabled={loading}
                        />
                    </div>
                    <div class="w-full">
                        <button
                                class="py-2 px-8 bg-red-600 hover:bg-red-800 focus:ring-offset-red-200 text-white w-full
                            transition ease-in duration-200 text-center text-base font-semibold shadow-md focus:outline-none
                            focus:ring-2 focus:ring-offset-2 rounded-lg cursor-pointer select-none disabled:opacity-50"
                                onclick={handleLogin}
                                disabled={loading}
                        >
                            {loading ? 'Loading...' : 'Login'}
                        </button>
                    </div>
                </div>
            </div>
        {:else}
            <div class="px-8 py-6 mt-4">
                <div class="flex flex-col justify-center items-center h-full select-none">
                    <div class="flex flex-col items-center justify-center gap-2 mb-8">
                        <div class="w-8 h-8 bg-gray-700 rounded-full flex items-center justify-center text-2xl">
                            ➕
                        </div>
                        <p class="m-0 text-[16px] font-semibold dark:text-white">
                            Create an Account
                        </p>
                        <span class="m-0 text-xs max-w-[90%] text-center text-[#8B8E98]">
                            Sign up to get started with our app.
                        </span>
                    </div>
                    <div class="w-full flex flex-col gap-2">
                        <label class="font-semibold text-xs text-gray-100">Username</label>
                        <input
                                bind:value={username}
                                placeholder="Username"
                                class="border rounded-lg px-3 py-2 mb-3 text-sm w-full outline-none dark:border-gray-500 dark:bg-gray-900"
                                disabled={loading}
                        />
                    </div>
                    <span class="m-0 text-xs max-w-[90%] text-center text-[#8B8E98] mb-2">
                        The password must be at least 8 characters long, have one uppercase letter, one lowercase letter, and one number.
                    </span>
                    <div class="w-full flex flex-col gap-2">
                        <label class="font-semibold text-xs text-gray-100">Password</label>
                        <input
                                bind:value={password}
                                placeholder="••••••••"
                                class="border rounded-lg px-3 py-2 mb-5 text-sm w-full outline-none dark:border-gray-500 dark:bg-gray-900"
                                type="password"
                                disabled={loading}
                        />
                    </div>
                    <div class="w-full flex flex-col gap-2">
                        <label class="font-semibold text-xs text-gray-100">Verify password</label>
                        <input
                                bind:value={password2}
                                placeholder="••••••••"
                                class="border rounded-lg px-3 py-2 mb-5 text-sm w-full outline-none dark:border-gray-500 dark:bg-gray-900"
                                type="password"
                                onkeydown={(e) => e.key === 'Enter' && !loading && handleRegister()}
                                disabled={loading}
                        />
                    </div>
                    <div class="w-full">
                        <button
                                class="py-2 px-8 bg-red-600 hover:bg-red-800 focus:ring-offset-red-200 text-white w-full
                            transition ease-in duration-200 text-center text-base font-semibold shadow-md focus:outline-none
                            focus:ring-2 focus:ring-offset-2 rounded-lg cursor-pointer select-none disabled:opacity-50"
                                onclick={handleRegister}
                                disabled={loading}
                        >
                            {loading ? 'Creating Account...' : 'Register'}
                        </button>
                    </div>
                </div>
            </div>
        {/if}
    </div>
</section>