<script setup>
const { getMonthAgo } = useDates()
const { fetchHistory } = useCurrencyHistory()
const { fetchActualRate, getRateForCurrency } = useActualCurrencyRate()
const currenciesStore = useCurrenciesStore()

onMounted(() => {
  updateActualRate()
  if (currenciesStore.shouldRefresh) {
     loadCurrencies()
  }
})

const selectedCurrency = ref("USD")
const actualRate = ref(null)
const { data: ratesData } = await fetchActualRate(selectedCurrency.value)
const updateActualRate = () => {
  if (ratesData.value) {
    actualRate.value = getRateForCurrency(ratesData.value, selectedCurrency.value)
  }
}
watch(selectedCurrency, () => {
  updateActualRate()
})
watch(ratesData, () => {
  updateActualRate()
})

const currencies = computed(() => currenciesStore.currencies)
const filteredCurrencies = computed(() => {
  return currencies.value.filter(currency => currency.code !== "RUB")
})

const loadCurrencies = async () => {
  try {
    await currenciesStore.fetchCurrencies()
  } catch (err) {
    console.error("Failed to load currencies", err)
  }
}

const { data: ratesHistory } = await fetchHistory(getMonthAgo())
const selectedCurrencies = ["USD", "EUR", "GBP"]
</script>


<template>
  <div class="currency-container">
    <div class="currency-layout">
      <div class="currency-card">
        <h1 class="currency-title">Актуальный курс</h1>

        <div class="currency-selector">
          <el-select
              v-model="selectedCurrency"
              size="large"
              filterable
              placeholder="Выберите валюту"
              style="width: 100%;"
          >
            <el-option
                v-for="currency in filteredCurrencies"
                :key="currency.code"
                :label="`${currency.name} (${currency.code})`"
                :value="currency.code"
            />
          </el-select>
        </div>

        <div class="currency-rate" v-if="actualRate !== null && actualRate !== undefined">
          <div class="rate-label">текущий курс</div>
          <div class="rate-value">{{ actualRate }}</div>
        </div>

        <div class="currency-error" v-else>
          <p>Не удалось загрузить курс</p>
        </div>
      </div>

      <div class="chart-container">
      <CurrencyChart
          :data="ratesHistory"
          :selected-currencies="selectedCurrencies"
          title="Динамика курсов за последний месяц"
      />
      </div>
    </div>
  </div>
</template>

<style scoped>
.currency-container {
  max-width: 100%;
  margin: 40px;
  padding: 0; /* УБРАНО: большой padding */
  justify-content: center; /* ДОБАВЛЕНО: выравнивание по центру по горизонтали */
  min-height: calc(100vh - 80px); /* ДОБАВЛЕНО: минимальная высота на весь экран минус margin */
}

.currency-layout {
  display: grid;
  grid-template-columns: 400px 1fr;
  gap: 32px;
  align-items: start;
}

.currency-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  border: 1px solid #eaeaea;
  width: 400px;
}

.currency-title {
  font-size: 24px;
  font-weight: 500;
  color: #1a1a1a;
  margin: 0 0 24px 0;
  text-align: center;
}

.currency-selector {
  margin-bottom: 24px;
}

.currency-rate {
  text-align: center;
  padding: 0;
}

.rate-value {
  font-size: 32px;
  font-weight: 600;
  color: #2c3e50;
}

.rate-label {
  font-size: 14px;
  color: #7f8c8d;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.currency-error {
  text-align: center;
  padding: 0;
  color: #95a5a6;
}

.chart-container {
  background: #ffffff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  border: 1px solid #eaeaea;
  min-height: 400px;
  width: 800px;
  margin-left: auto;
}
</style>