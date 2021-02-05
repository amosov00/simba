export default async function ({ app, store }) {
  if (app.$cookies.get('token') && !store.getters.user) {
    await app.$authFetchUser()
  }
}
