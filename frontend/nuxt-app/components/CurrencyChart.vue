<script setup lang="ts">
interface CurrencyRate {
  currency_code: string
  rate: number
}

interface ApiResponse {
  base: string
  rates: {
    [date: string]: CurrencyRate[]
  }
}

interface Props {
  data: ApiResponse
  selectedCurrencies: string[]
  title?: string
  height?: string
  width?: string
}

const props = withDefaults(defineProps<Props>(), {
  title: 'Курсы валют',
  height: '400px',
  width: '100%'
})

const chartStyle = computed(() => ({
  height: props.height,
  width: props.width
}))


const chartOption = computed(() => {
  const dates = Object.keys(props.data.rates)
    .sort((a, b) => new Date(a).getTime() - new Date(b).getTime())

  const series = props.selectedCurrencies.map(currencyCode => {
    const rates = dates.map(date => {
      const rateData = props.data.rates[date]?.find(
        rate => rate.currency_code === currencyCode
      )
      return rateData ? rateData.rate : null
    })

    return {
      name: currencyCode,
      type: 'line',
      data: rates,
      smooth: true,
      symbol: 'circle',
      symbolSize: 6,
      lineStyle: {
        width: 2
      },
      emphasis: {
        focus: 'series'
      }
    }
  })

  return {
    title: {
      text: props.title,
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      }
    },
    legend: {
      data: props.selectedCurrencies,
      bottom: 0
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: dates,
      axisLabel: {
        rotate: 45
      }
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        formatter: '{value}'
      }
    },
    series
  }
})
</script>

<template>
  <div class="currency-chart">
    <VChart
      :option="chartOption"
      :autoresize="true"
      :style="chartStyle"
    />
  </div>
</template>

<style scoped>
.currency-chart {
  width: 100%;
}
</style>
