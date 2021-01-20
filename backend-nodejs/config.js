module.exports = {
  HOST: process.env.HOST,
  PORT: process.env.PORT || 8080,
  ENV: process.env.ENV,
  NODE_ENV: process.env.NODE_ENV,
  IS_PRODUCTION: process.env.ENV === "production",
  SENTRY_DSN: process.env.SENTRY_DSN_NODEJS,
  COMMIT: process.env.COMMIT,
}
