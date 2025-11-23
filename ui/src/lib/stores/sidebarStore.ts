import { writable } from 'svelte/store';

interface SidebarSide {
    side: string;
}

function createSidebarStore() {
    const { subscribe, set, update } = writable<SidebarSide | null>(null);

    return {
        subscribe,
        setSide: (side: string) => {
            set({ side });
            localStorage.setItem('side', side);
        },
        getFromLocalStorage: () => {
            const side = localStorage.getItem('side');
            if (side) set({ side });
        },
        set
    };
}

export const sideStore = createSidebarStore();
