export const useCurrencyHistory = () => {
    const apiUrl = useRuntimeConfig().public.apiUrl
    const { getToday } = useDates()

    const fetchHistory = (startDate: string, endDate: string = getToday()) => {
        const queryParams = new URLSearchParams()
        queryParams.append('start_date', startDate)
        queryParams.append('end_date', endDate)

        const url = `${apiUrl}/api/rates/history?${queryParams.toString()}`

        return useAsyncData(
            `history-${startDate}-${endDate}`,
            () => $fetch(url),
            {
                default: () => ({}),
            }
        )
    }
    return { fetchHistory }
}