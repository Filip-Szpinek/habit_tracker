import { writable } from 'svelte/store';
import type {Habit, LogDate, Log} from '../types/types'

interface HabitsState {
    habits: Habit[];
    loading: boolean;
    error: string | null;
}

function createHabitsStore() {
    const { subscribe, set, update } = writable<HabitsState>({
        habits: [],
        loading: false,
        error: null
    });

    return {
        subscribe,

        async fetchHabits() {
            update(state => ({ ...state, loading: true, error: null }));

            try {
                const response = await fetch('/api/habits', {
                    credentials: 'include'
                });

                if (!response.ok) {
                    throw new Error('Failed to fetch habits');
                }

                const data = await response.json();

                update(state => ({
                    ...state,
                    habits: data.habits || [],
                    loading: false
                }));

                return data.habits;
            } catch (error) {
                update(state => ({
                    ...state,
                    loading: false,
                    error: error instanceof Error ? error.message : 'Unknown error'
                }));
                console.error('Error fetching habits:', error);
                return [];
            }
        },

        async addHabit(habitData: {
            name: string;
            description: string;
            frequency: string;
        }) {
            try {
                const formData = new FormData();
                formData.append('name', habitData.name);
                formData.append('description', habitData.description);
                formData.append('frequency', habitData.frequency);

                const response = await fetch('/add-habit', {
                    method: 'POST',
                    credentials: 'include',
                    headers: {
                        'Accept': 'application/json'  // Add this!
                    },
                    body: formData
                });

                if (!response.ok) {
                    throw new Error('Failed to add habit');
                }

                await this.fetchHabits();
                return true;
            } catch (error) {
                console.error('Error adding habit:', error);
                return false;
            }
        },

        async toggleHabit(habitId: number) {
            try {
                const response = await fetch(`/check-habit/${habitId}`, {
                    method: 'POST',
                    credentials: 'include'
                });

                if (!response.ok) {
                    throw new Error('Failed to toggle habit');
                }

                await this.fetchHabits();
                return true;
            } catch (error) {
                console.error('Error toggling habit:', error);
                return false;
            }
        },

        async deleteHabit(habitId: number) {
            try {
                const response = await fetch(`/delete-habit/${habitId}`, {
                    method: 'POST',
                    credentials: 'include'
                });

                if (!response.ok) {
                    throw new Error('Failed to delete habit');
                }

                update(state => ({
                    ...state,
                    habits: state.habits.filter(h => h.id !== habitId)
                }));

                return true;
            } catch (error) {
                console.error('Error deleting habit:', error);
                return false;
            }
        },

        clear() {
            set({ habits: [], loading: false, error: null });
        }
    };
}

export const habitsStore = createHabitsStore();