export interface Habit {
    id: number,
    name: string,
    description: string,
    frequency: string,
    logs: LogDate[]
}

export interface LogDate {
    date: string,
    logs: Log[]
}

export interface Log {
    completed: boolean
}