import _ from 'lodash'
import moment from 'moment'

import { ToastProgrammatic as Toast } from 'buefy'

export const state = () => ({
  invoices: [],
  adminInvoices: [],
})

export const getters = {
  invoices: (s) => s.invoices,
  adminInvoices: (s) => s.adminInvoices,
}

export const mutations = {
  addInvoice: (state, invoice) => (state.invoices = _.uniqBy([invoice, ...state.invoices], '_id')),
  setInvoices: (state, data) => (state.invoices = data),
  setAdminInvoices: (state, data) => (state.adminInvoices = data),
}

export const actions = {
  async createTransaction({}, data) {
    return await this.$axios
      .post('/invoices/', { invoice_type: data })
      .then((res) => {
        //Toast.open({message: 'Transaction created!', type: 'is-primary'});
        return res.data
      })
      .catch((_) => {
        Toast.open({
          message: this.$i18n.t('exchange.error_creating_invoice'),
          type: 'is-danger',
        })
        return false
      })
  },

  async updateTransaction({}, data) {
    let data_to_send = {
      target_eth_address: data.eth_address,
      btc_amount: data.btc_amount,
      simba_amount: data.simba_amount,
    }

    if (data.btc_address) {
      data_to_send['target_btc_address'] = data.btc_address
    }

    return await this.$axios
      .put(`/invoices/${data.id}/`, data_to_send)
      .then((res) => {
        //Toast.open({message: 'Transaction updated!', type: 'is-primary'});
        return res.data
      })
      .catch((_) => {
        Toast.open({
          message: this.$i18n.t('exchange.error_updating_invoice'),
          type: 'is-danger',
        })
        return false
      })
  },

  async manualTransaction({}, data) {
    return await this.$axios
      .post(`/invoices/${data.id}/transaction/`, {
        btc_transaction_hash: data.transaction_hash,
      })
      .then((res) => {
        Toast.open({ message: res.data, type: 'is-primary' })
        return res.data
      })
      .catch((err) => {
        Toast.open({
          message: err.response.data[0].message,
          type: 'is-danger',
        })
        return false
      })
  },

  async confirmTransaction({}, id) {
    return await this.$axios
      .post(`/invoices/${id}/confirm/`)
      .then((res) => res.data)
      .catch((_) => {
        Toast.open({
          message: this.$i18n.t('exchange.error_confirming_invoice'),
          type: 'is-danger',
        })
        return false
      })
  },

  async fetchInvoices({ commit }) {
    return await this.$axios
      .get('/invoices/')
      .then((res) => {
        commit('setInvoices', res.data)
      })
      .catch(() => {})
  },

  async fetchAdminInvoices({ commit }, params) {
    return await this.$axios
      .get('/admin/invoices/', { params: params })
      .then((res) => {
        let data = res.data
        data.forEach((el) => {
          el.created_at = moment(el.created_at).utc().valueOf()
        })
        commit('setAdminInvoices', data)
        return data
      })
      .catch(() => {})
  },

  async fetchAdminSingleInvoice({}, id) {
    return await this.$axios
      .get(`/admin/invoices/${id}/`)
      .then((res) => res.data)
      .catch(() => {})
  },

  async fetchSingle({ commit }, id) {
    return await this.$axios
      .get(`/invoices/${id}/`)
      .then((res) => res.data)
      .catch((_) => false)
  },
}
