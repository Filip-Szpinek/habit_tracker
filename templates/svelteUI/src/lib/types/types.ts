export interface habit {
    id: number,
    title: string,
    description?: string,
    frequency: 'daily' | 'weekly' | 'monthly',
    amount: number,
    startDate: string,
    endDate?: string,
    logs: habitDateLog[]
}

export interface AddHabit {
    title: string,
    description?: string,
    frequency: 'daily' | 'weekly' | 'monthly',
    amount: number,
    startDate: string,
    endDate?: string
}

export interface habitDateLog{
    date: string,
    logs: habitLog[]
}

export interface habitLog {
    time?: string,
    count: number,
    completed: boolean
}