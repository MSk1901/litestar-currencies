export const useDates = () => {
    const getToday = (): string => {
        const date = new Date()
        return date.toISOString().split('T')[0] as string
    }

    const getMonthAgo = (): string => {
        const date = new Date()
        date.setDate(date.getDate() - 30) // Отнимаем 30 дней
        return date.toISOString().split('T')[0] as string
    }
    return {
        getToday,
        getMonthAgo
    }
}