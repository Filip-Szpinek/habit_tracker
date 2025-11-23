export interface habit {
    id: number,
    name: string,
    description: string,
    frequency: 'daily' | 'weekly' | 'monthly',
}

export interface habitLog {
    is_done: boolean,
}