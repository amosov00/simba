import _ from "lodash";

import { ToastProgrammatic as Toast } from 'buefy'

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
      //Toast.open({message: 'Transaction created!', type: 'is-primary'});
      return res.data;
    }).catch(_ => {
      Toast.open({message: 'Error creating invoice!', type: 'is-danger'});
      return false
    })
  },

  async updateTransaction({}, data) {
    let data_to_send = {
      "target_eth_address": data.eth_address,
      "target_btc_address": data.btc_address,
      "btc_amount": data.simba_amount,
      "simba_amount": data.simba_amount,
    }

    return await this.$axios.put(`/invoices/${data.id}/`, data_to_send).then(res => {
      //Toast.open({message: 'Transaction updated!', type: 'is-primary'});
      return res.data;
    }).catch(_ => {
      Toast.open({message: 'Error updating invoice!', type: 'is-danger'});
      return false
    })
  },

  async manualTransaction({}, data) {
    return await this.$axios.post(`/invoices/${data.id}/transaction/`, { btc_transaction_hash: data.transaction_hash}).then(res => {
      Toast.open({message: res.data, type: 'is-primary'});
      return res.data
    })
      .catch(err => {
        Toast.open({message: err.response.data[0].message, type: 'is-danger'});
        return false
      })
  },

  async confirmTransaction({}, id) {
    return await this.$axios.post(`/invoices/${id}/confirm/`).then(res => res.data)
      .catch(_ => {
        Toast.open({message: 'Error confirming invoice!', type: 'is-danger'});
        return false
      })
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
