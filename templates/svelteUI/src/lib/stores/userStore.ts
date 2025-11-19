import { writable } from 'svelte/store';

interface User {
    username: string;
}

function createUserStore() {
    const { subscribe, set, update } = writable<User | null>(null);

    return {
        subscribe,
        login: (username: string) => set({ username }),
        logout: () => set(null),
        set
    };
}

export const userStore = createUserStore();