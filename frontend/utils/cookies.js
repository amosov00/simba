// TODO hotfix
export const getCookieToken = (app) => {
  return app.$cookies.get('simbaToken')
}

export const setCookieToken = (app, token) => {
  app.$cookies.set('simbaToken', token, {
    path: '/',
    maxAge: 60 * 60 * 24 * 7,
    domain: document.domain,
  })
}

export const clearCookieToken = (app) => {
  app.$cookies.remove('simbaToken', {
    path: '/',
    maxAge: 60 * 60 * 24 * 7,
    domain: document.domain,
  })
  // Double check
  if (app.$config.isProduction) {
    app.$cookies.remove('simbaToken', {
      path: '/',
      maxAge: 60 * 60 * 24 * 7,
      domain: 'my.simba.storage',
    })
  }
}
