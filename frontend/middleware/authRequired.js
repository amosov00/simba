export default async function ({ store, redirect }) {
  if (!store.getters.user) {
    await redirect('/')
  }
}
