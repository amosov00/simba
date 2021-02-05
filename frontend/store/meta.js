import Vue from 'vue'

export const state = () => ({
  state: {
    meta: [],
  },
})

export const getters = {
  meta: (state) => state.meta,
}

export const mutations = {
  setMeta: (state, data) => {
    Vue.set(state, 'meta', data)
  },
}

export const actions = {
  async fetchMeta({ commit }) {
    return await this.$axios
      .get('/admin/meta/')
      .then((res) => {
        commit('setMeta', res.data)
      })
      .catch(() => false)
  },

  async updateMeta({}, payload) {
    return await this.$axios
      .put(`/admin/meta/${payload.slug}/`, payload.data)
      .then(() => true)
      .catch(() => false)
  },

  async invoiceDecision({}, data) {
    return await this.$axios
      .post(`/admin/invoices/${data.id}/${data.type}/`)
      .then(() => true)
      .catch(() => false)
  },

  async fetchInvoiceSstTransactions({}, id) {
    return await this.$axios
      .get(`/admin/invoices/${id}/sst_transactions/`)
      .then((res) => res.data)
      .catch(() => [])
  },
}
