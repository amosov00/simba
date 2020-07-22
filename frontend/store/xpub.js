export const state = () => ({
  state: {
    xpubList: []
  }
})

export const getters = {
  xpubList: state => state.xpubList
}

export const mutations = {
  setXpubList: (state, data) => (state.xpubList = data)
}

export const actions = {
  btcXpubFetchAll({commit}) {
    return this.$axios.get('/admin/btc-xpub/')
      .then(res => commit('setXpubList', res.data))
      .catch(() => {})
  },

  async btcXpubUpdateSingle({}, payload) {
    return await this.$axios.put(`/admin/btc-xpub/${payload.id}/`, payload.data)
      .then(() => true)
      .catch(() => false)
  }
}
