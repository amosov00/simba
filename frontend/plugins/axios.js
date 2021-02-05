export default function ({ $axios, app }) {
  $axios.setToken(app.$cookies.get('token'), 'Bearer')

  $axios.onError(async (error) => {
    switch (error.response.status) {
      case 401:
        await app.$authLogout()
        break
      default:
        break
    }
  })
}
