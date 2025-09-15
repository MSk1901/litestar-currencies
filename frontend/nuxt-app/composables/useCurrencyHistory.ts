export const useCurrencyHistory = () => {
    const config = useRuntimeConfig()
    const apiUrl = useRequestEvent() ? config.apiUrl : config.public.apiUrl
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