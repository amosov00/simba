const HOST = process.env.HOST
const PORT = process.env.PORT || 8080

const ENV = process.env.ENV
const NODE_ENV = process.env.NODE_ENV
const IS_PRODUCTION = ENV === "production"
const COMMIT = process.env.COMMIT

const SENTRY_DSN = process.env.SENTRY_DSN_NODEJS


export {HOST, PORT, ENV, NODE_ENV, IS_PRODUCTION, SENTRY_DSN, COMMIT}