import _ from "lodash";

export const state = () => ({
  status: 'offline',
  address: ''
});

export const getters = {
  status: s => s.status,
  address: s => s.address,
};

export const mutations = {
  setStatus: (state, data) => (state.status = data),
  setAddress: (state, data) => (state.address = data),
};

export const actions = {
  set_status({commit}, payload) {
    commit('setStatus', payload)
  },
  set_address({commit}, payload) {
    commit('setAddress', payload)
  },
};
