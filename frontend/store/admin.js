export const state = () => ({
  users: []
})

export const getters = {}

export const mutations = {
  setUsers: (state, payload) => state.users = payload,
}

export const actions = {
  async fetchUsers({commit}, query) {
    return await this.$axios
      .get(
        `/admin/users/`,
        query
          ? {
              params: {
                q: query,
              },
            }
          : {}
      )
      .then((res) => {
        commit('setUsers', res.data)
        return res.data
      })
      .catch(() => {})
  },

  async exportUsers({}, query) {
    return await this.$axios
      .get(`/admin/users/`, {
        params: {
          q: query || null,
          format: 'excel',
        },
        responseType: 'blob',
      })
      .then((res) => {
        return res.data
      })
      .catch(() => {
        return null
      })
  },

  async fetchUserById({}, id) {
    return await this.$axios
      .get(`/admin/users/${id}/`)
      .then((res) => {
        return res.data
      })
      .catch(() => {})
  },
  async fetchKYCUserById({}, id) {
    return await this.$axios
      .get(`/admin/users/${id}/kyc/status/`)
      .then((res) => {
        return res.data
      })
      .catch(() => {})
  },
}
