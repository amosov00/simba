import _ from "lodash";

export const state = () => ({
  invoices: []
});

export const getters = {
  invoices: s => s.invoices,
};

export const mutations = {
  setInvoices: (state, data) => (state.invoices = data),
};

export const actions = {
  async createTransaction({}, data) {
    return await this.$axios.post('/invoices/', { invoice_type: data }).then(res =>{
      return res.data;
    }).catch(_ => {
      return false
    })
  },

  async manualTransaction({}, data) {
    return await this.$axios.post(`/invoices/${data.id}/transaction/`, { btc_transaction_hash: data.transaction_hash}).then(res => res.data)
      .catch(_ => false)
  },

  async fetchInvoices({commit}, payload) {
    return await this.$axios.get('/invoices/').then(res => {
      commit('setInvoices', res.data)
      return true;
    }).catch(_ => false)
  },

  async fetchSingle({commit}, id) {
    return await this.$axios.get(`/invoices/${id}/`).then(res => res.data).catch(_ => false)
  },
};
