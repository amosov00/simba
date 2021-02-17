export const state = () => ({})

export const getters = {}

export const mutations = {}

export const actions = {
  async fetchUsers({}, query) {
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
}
