export const useActualCurrencyRate = () => {
    const config = useRuntimeConfig()
    const apiUrl = useRequestEvent() ? config.apiUrl : config.public.apiUrl

    const fetchActualRate = () => {
        const url = `${apiUrl}/api/rates/actual`
        return useFetch(url);
    }

    const getRateForCurrency = (ratesData: any, currencyCode: string): number | null => {
        if (!ratesData?.rates) return null

        const currencyRate = ratesData.rates.find((rate: any) =>
            rate.currency_code === currencyCode.toUpperCase()
        )

        return currencyRate ? currencyRate.rate : null
    }
    return {
        fetchActualRate,
        getRateForCurrency
    }
}