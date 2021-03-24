const initialState = {
  invoice: {},
  invoiceId: null,
  fetchInvoiceDataLoop: true,
  currentStepComponent: '',
  currentStepIndicatorIndex: 0,
  operation: '',
  limits: {},
  currencyRate: {},
  addresses: {
    eth: null,
    btc: null,
  }, // eth and btc address
  adminEthHash: null,
}

export const state = () => {
  return Object.assign({}, initialState)
}

export const getters = {
  tradeData: (s) => s,
  limits: (s) => s.limits,
  isBuyInvoice: (s) => s.operation === 'buy',
  ethTxByEvent: (s) => (event) => {
    let filtered = s.eth_txs.filter((i) => i.event === event)
    return filtered.length > 0 ? filtered[0] : null
  },
}

export const mutations = {
  setOperation: (state, payload) => (state.operation = payload),
  setFetchInvoiceDataLoop: (state, payload) => (state.fetchInvoiceDataLoop = payload),
  setInvoice: (state, payload) => (state.invoice = payload),
  setInvoiceId: (state, payload) => (state.invoiceId = payload),
  setCurrentStepComponent: (state, payload) => (state.currentStepComponent = payload),
  setCurrentStepIndicatorIndex: (state, payload) => (state.currentStepIndicatorIndex = payload),
  setAddresses: (state, payload) => (state.addresses = payload),
  setAdminEthHash: (state, payload) => (state.adminEthHash = payload),
  setNextStep: (state, payload) => {
    state.currentStepComponent = payload
    state.currentStepIndicatorIndex += 1
  },
  setLimits: (state, payload) => {
    state.limits = payload
  },
  setCurrencyRate: (state, payload) => {
    state.currencyRate = payload
  },
  clearState: (state) => {
    state = Object.assign(state, initialState)
  },
}

export const actions = {
  fetchAdminEthAddress({ commit }) {
    return this.$axios
      .get('/meta/eth/admin-address/')
      .then((res) => {
        commit('setAdminEthHash', res.data.address)
      })
      .catch(() => false)
  },
  async fetchLimits({ commit }) {
    return this.$axios
      .get('/account/kyc/limit/')
      .then((res) => {
        commit('setLimits', res.data)
      })
      .catch(() => false)
  },
  async fetchCurrencyRate({ commit }) {
    return this.$axios
      .get('/meta/currency-rate/')
      .then((res) => {
        commit('setCurrencyRate', res.data)
      })
      .catch(() => false)
  },
}
