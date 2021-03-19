export const state = () => ({
  invoice_id: '',
  operation: 1,
  eth_address: '',
  btc_redeem_wallet: '',
  admin_eth_address: '',
  simba: 0,
  btc: 0,
  btc_amount_proceeded: 0,
  target_eth: '',
  tx_hash: '',
  tx_hash_redeem: '',
  simba_issued: 0,
  eth_txs: [],
  limits: {}
})

export const getters = {
  tradeData: (s) => s,
  limits: (s) => s.limits,
  ethTxByEvent: (s) => (event) => {
    let filtered = s.eth_txs.filter((i) => i.event === event)
    return filtered.length > 0 ? filtered[0] : null
  },
}

export const mutations = {
  setTradeData: (state, payload) => {
    state[payload.prop] = payload.value
  },
  setLimits: (state, payload) => {
    state.limits = payload
  },
  setRate: (state, payload) => {
    state.limits = {
      ...state.limits,
      ...payload
    }
  }
}

export const actions = {
  fetchAdminEthAddress({ commit }) {
    return this.$axios.get('/meta/eth/admin-address/').then((res) => {
      commit('setTradeData', { prop: 'admin_eth_address', value: res.data.address })
    })
  },
  async fetchLimits({commit}) {
    const limitRes = await this.$axios.get('/account/kyc/limit/')
    const rateRes = await this.$axios.get('/meta/currency-rate/')
    commit('setLimits', limitRes.data)
    commit('setRate', rateRes.data)
  }
}
