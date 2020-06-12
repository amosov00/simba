export default {
  mode: 'spa',

  head: {
    title: 'Simba — Swiss Quality Stablecoin',
    meta: [
      {charset: 'utf-8'},
      {name: 'viewport', content: 'width=device-width, initial-scale=1'},
      {hid: 'description', name: 'description', content: ''}
    ],
    link: [
      {rel: "icon", type: "image/x-icon", href: "/favicon.ico"},
      {rel:"stylesheet", href:"https://fonts.googleapis.com/css2?family=Roboto&display=swap"}
    ]
  },

  loading: {color: '#0495FB'},

  css: [
    {src: '~/assets/scss/main.sass', lang: 'sass'},
    {src: '~/assets/scss/transition.scss', lang: 'scss'},
    {src: '@fortawesome/fontawesome-free/css/all.css', lang: 'css'},
  ],

  plugins: [
    '~/plugins/auth.js',
    '~/plugins/axios.js',
  ],
  modules: [
    '@nuxtjs/axios',
    '@nuxtjs/dotenv',
    '@nuxtjs/sentry',
    ['nuxt-buefy', {css: false}],
    'cookie-universal-nuxt',
  ],
  axios: {
    baseURL: process.env.API_URL || 'https://simba-dev.elastoo.com/api/',
  },
  buildModules: [
    '@nuxtjs/dotenv'
  ],
  server: {
    host: '0.0.0.0',
  },
  dotenv: !process.env.ENV ? {
    filename: '.env.local',
  } : {},
  sentry: {
    dsn: process.env.SENTRY_DNS_FRONT || '',
  },
  build: {
    extend(config, ctx) {
    }
  }
}
