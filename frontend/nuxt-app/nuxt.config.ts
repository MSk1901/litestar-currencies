export default defineNuxtConfig({
    compatibilityDate: '2025-07-15',
    devtools: {enabled: true},
    app: {
        head: {
            title: 'Litestar currencies',
        }
    },
    css: ['@/assets/css/global.css'],
    modules: ['@element-plus/nuxt', '@nuxt/fonts',],
    fonts: {
        families: [
            {"name": "Montserrat", "provider": "google"}
        ]
    }
})