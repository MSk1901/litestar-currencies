export default defineNuxtConfig({
    compatibilityDate: "2025-07-15",
    devtools: {enabled: true},
    app: {
        head: {
            title: "Litestar currencies",
        }
    },
    runtimeConfig: {
        apiUrl: "",
        public: {
            apiUrl: "",
        }
    },
    nitro: {
        prerender: {
            crawlLinks: false
        },
    },
    css: ["@/assets/css/global.css"],
    modules: ["@element-plus/nuxt", "@nuxt/fonts", "@pinia/nuxt", "nuxt-echarts"],
    fonts: {
        families: [
            {"name": "Montserrat", "provider": "google"}
        ]
    },
    echarts: {
    renderer: 'svg',
    charts: ['LineChart'],
    components: [
      'GridComponent',
      'TooltipComponent',
      'LegendComponent',
      'TitleComponent',
      'MarkLineComponent',
      'MarkPointComponent',
      'DataZoomComponent'
    ],
  }
})