export default function ({ store, redirect, app }) {
  let user = store.state.user

  if (!user || user['is_superuser'] !== true) {
    redirect('/')
  } else {
    return true
  }
}
