import {getCookieToken} from "~/utils/cookies";

export default async function ({ app, store }) {
  if (!store.getters.user && getCookieToken(app)) {
    await app.$authFetchUser()
  }
}
