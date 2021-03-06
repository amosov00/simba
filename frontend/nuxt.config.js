export default {
  ssr: false,
  target: 'server',

  head: {
    title: 'Simba — Swiss Quality Stablecoin',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: 'Simba Storage' },
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
      {
        rel: 'stylesheet',
        href: 'https://fonts.googleapis.com/css2?family=Roboto:wght@100;300;400;500;700;900&display=swap',
      },
      {
        href: 'https://fonts.googleapis.com/css2?family=Didact+Gothic&display=swap',
        rel: 'stylesheet',
      },
      { href: '/logo-lg.png', rel: 'shortcut icon' },
    ],
  },

  loadingIndicator: {
    name: 'pulse',
    color: '#e0b72e',
  },

  css: [
    { src: '~/assets/scss/main.sass', lang: 'sass' },
    { src: '~/assets/scss/transition.scss', lang: 'scss' },
    { src: '@fortawesome/fontawesome-free/css/all.css', lang: 'css' },
  ],

  plugins: [
    '~/plugins/auth.js',
    '~/plugins/axios.js',
    '~/plugins/vee-validate.js',
    '~/plugins/contract.js',
    '~/plugins/web3.js',
    '~/plugins/i18n.js',
  ],
  modules: [
    '@nuxtjs/axios',
    '@nuxtjs/sentry',
    'cookie-universal-nuxt',
    ['nuxt-buefy', { css: false }],
    [
      'nuxt-i18n',
      {
        locales: [
          {
            code: 'ru',
            file: 'rus.js',
          },
          {
            code: 'en',
            file: 'eng.js',
          },
        ],
        lazy: true,
        langDir: 'lang/',
      },
    ],
  ],
  server: {
    host: '0.0.0.0',
  },
  sentry: {
    initialize: true,
    config: {
      environment: process.env.NODE_ENV,
    },
  },
  publicRuntimeConfig: {
    domain: process.env.DOMAIN || 'my.simba.storage',
    sumsubURL: process.env.API_URL_SUMSUB,
    isProduction: process.env.NODE_ENV === 'production',
  },
  env: {
    isProduction: process.env.NODE_ENV === 'production',
  },
  i18n: {
    strategy: 'no_prefix',
    detectBrowserLanguage: {
      useCookie: true,
      cookieKey: 'app_lang',
      alwaysRedirect: false,
      fallbackLocale: 'en',
    },
  },
  build: {
    extend(config, ctx) {},
  },
}
