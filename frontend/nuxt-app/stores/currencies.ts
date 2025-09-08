export const useCurrenciesStore = defineStore('currencies', {
  state: () => ({
    currencies: [] as any[],
    lastFetched: null as Date | null,
    isLoading: false,
    error: null as string | null
  }),

  getters: {
    shouldRefresh: (state) => {
      if (!state.lastFetched) return true
      const now = new Date()
      const diffInHours = (now.getTime() - state.lastFetched.getTime()) / (1000 * 60 * 60)
      return diffInHours >= 24
    },
    getCurrencies: (state) => state.currencies,
    getLoading: (state) => state.isLoading,
    getError: (state) => state.error
  },

actions: {
    async fetchCurrencies() {
      // Проверяем наличие данныx в localStorage
      if (import.meta.client) {
        const cached = localStorage.getItem('currencies-cache')
        const cacheTime = localStorage.getItem('currencies-cache-time')

        if (cached && cacheTime) {
          const now = new Date()
          const cacheDate = new Date(parseInt(cacheTime))
          const diffInHours = (now.getTime() - cacheDate.getTime()) / (1000 * 60 * 60)

          if (diffInHours < 24) {
            this.currencies = JSON.parse(cached)
            this.lastFetched = cacheDate
            return this.currencies
          }
        }
      }

      if (!this.shouldRefresh && this.currencies.length > 0) {
        return this.currencies
      }

      this.isLoading = true
      this.error = null

      try {
        const apiUrl = useRuntimeConfig().public.apiUrl
        const currencies_list = await $fetch(`${apiUrl}/api/currencies`)

        this.currencies = currencies_list as any[]
        this.lastFetched = new Date()

        if (import.meta.client) {
          localStorage.setItem('currencies-cache', JSON.stringify(currencies_list))
          localStorage.setItem('currencies-cache-time', Date.now().toString())
          console.log("💾 Сохранили в localStorage")
        }

        return this.currencies
      } catch (err: any) {
        this.error = err.message || 'Failed to fetch currencies'
        throw err
      } finally {
        this.isLoading = false
      }
    },

    clearCache() {
      this.lastFetched = null
      this.currencies = []
      if (import.meta.client) {
        localStorage.removeItem('currencies-cache')
        localStorage.removeItem('currencies-cache-time')
      }
    }
  }
})