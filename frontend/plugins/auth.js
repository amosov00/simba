export default ({ app, redirect, route }, inject) => {
  inject('authLogin', async (email, password, pin_code) => {
    return await app.$axios
      .post('/account/login/', {
        email: email,
        password: password,
        pin_code: pin_code,
      })
      .then(async (resp) => {
        app.$axios.setToken(resp.data.token, 'Bearer')
        app.$cookies.set('token', resp.data.token, {
          path: '/',
          maxAge: 60 * 60 * 24 * 7,
          domain: document.domain,
        })
        await app.store.dispatch('getUser')
        redirect('/exchange')
        return true
      })
      .catch((resp) => {
        return resp
      })
  })
  inject('authLogout', async () => {
    app.store.commit('deleteUser')
    await app.$axios.setToken(null)
    await app.$cookies.remove('token')
    setTimeout(()=>{
      redirect('/')
    })
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
