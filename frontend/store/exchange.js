import _ from "lodash";

export const state = () => ({
  invoice_id: '',
  operation: 1,
  eth_address: '',
  btc_target_wallet: '',
  simba: 0,
  btc: 0,
  no_create: false,
  btc_amount_proceeded: 0,
  target_eth: '',
  tx_hash: '',
  simba_issued: 0
});

export const getters = {
  tradeData: s => s
};

export const mutations = {
  setTradeData: (state, payload) => {
    state[payload.prop] = payload.value
  },
};

export const actions = {
};
