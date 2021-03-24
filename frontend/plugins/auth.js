import {clearCookieToken, setCookieToken} from "~/utils/cookies";

export default ({ app, redirect, route }, inject) => {
  inject('authLogin', async (email, password, pin_code) => {
    return await app.$axios
      .post('/account/login/', {
        email: email,
        password: password,
        pin_code: pin_code,
      })
      .then(async (resp) => {
        if (!resp) {
          return false
        }
        app.$axios.setToken(resp.data.token, 'Bearer')
        setCookieToken(app, resp.data.token)
        await app.store.dispatch('getUser')
        await redirect('/exchange')
        return true
      })
      .catch((resp) => {
        return resp
      })
  })
  inject('authLogout', async () => {
    app.store.commit('deleteUser')
    await app.$axios.setToken(null, 'Bearer')
    await clearCookieToken(app)
    // window.location.href = '/'
  })
  inject('authFetchUser', async () => {
    return app.$axios
      .get('/account/user/')
      .then((response) => {
        if (response && response.status === 200) {
          app.store.commit('setUser', response.data)
        } else {
          if (route.path !== '/') {
            redirect('/')
          }
        }
      })
      .catch((err) => {
        console.error(err)
      })
  })
  inject('userIsLoggedIn', () => {
    return app.store.getters.user
  })
  inject('userIsStaff', () => {
    return app.store.getters.user && app.store.getters.user.is_staff
  })
  inject('userIsSuperuser', () => {
    if (app.store.getters.user) {
      return app.store.getters.user.is_superuser
    }
    return false
  })
}
