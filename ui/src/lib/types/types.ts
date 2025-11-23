export interface habit {
    id: number,
    title: string,
    description: string,
    frequency: 'daily' | 'weekly' | 'monthly',
    amount: number,
    logs: logDate[]
}

export interface logDate {
    date: string,
    logs: habitLog[]
}

export interface habitLog {
    time?: string,
    completed: boolean,
    count: number
}