import _ from "lodash";

export const state = () => ({
  operation: 1,
  eth_address: '',
  simba: 0,
  btc: 0
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
