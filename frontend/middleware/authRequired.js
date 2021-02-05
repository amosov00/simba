export default async function ({ store, redirect, app }) {
  let user = store.state.user

  if (!user) {
    redirect('/')
  }
}
