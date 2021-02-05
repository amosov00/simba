export default async function ({ app, store }) {
  if (!store.getters.user && app.$cookies.get('token')) {
    await app.$authFetchUser()
  }
}
