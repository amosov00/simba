import _ from "lodash";

export const state = () => ({
  user: null,
  btc_address: '',
  contract: '',
  tradeData: {
    simba: 0,
    btc: 0
  }
});

export const getters = {
  user: s => s.user,
  btc_address: s => s.btc_address,
  contract: s => s.contract,
  tradeData: s => s.tradeData
};

export const mutations = {
  setUser: (state, user) => (state.user = user),
  setBtcAddress: (state, btc_address) => (state.btc_address = btc_address),
  deleteUser: state => (state.user = null),
  setContract: (state, data) => (state.contract = data),
  setTradeData: (state, data) => (state.tradeData = data),
};

export const actions = {
  async fetchContracts({commit}) {
    return await this.$axios.get('/meta/eth/contract/').then(res => {
      commit('setContract', res.data)
      return true
    }).catch(_ => false)
  },

  async activateAccount({}, data) {
    if (!data) return false;

    return await this.$axios
      .post("/account/verify/", data)
      .then(resp => {
        return true;
      })
      .catch(_ => {
        return false
      });
  },

  async getUser({commit}) {
    return await this.$axios.get('/account/user/').then(resp => {
      if(resp.status === 200 ){
        commit('setUser', resp.data)
        return true
      }

      return false
    }).catch(_ => false)
  },


  async getBtcAddress({ commit }) {
    return await this.$axios.get('/account/btc-address/')
      .then(resp => {
        commit('setBtcAddress', resp.data.address);
        return true;
      }).catch(_ => false)
  },

  async signUp({ commit }, data) {
    if (!data) return false;
    return await this.$axios
      .post("/account/signup/", data)
      .then(resp => {
        return true;
      })
      .catch(_ => {
        return false
      });
  },
  async changeProfile({}, data) {
    return await this.$axios.put("/account/user/", JSON.stringify(data))
      .then(_ => {
        return true;
      })
      .catch(err => {
        return false;
      });
  },
  async changePassword({}, data) {
    return await this.$axios.post("/account/change_password/", data)
      .then(_ => {
        return true;
      })
      .catch(err => {
        return false;
      });
  },
  async startRecover({}, data) {
    return await this.$axios.post("/account/recover/", data)
      .then(_ => {
        return true;
      })
      .catch(err => {
        return false;
      });
  },
  async finishRecover({}, data) {
    return await this.$axios.put("/account/recover/", data)
      .then(_ => {
        return true;
      })
      .catch(err => {
        return false;
      });
  },
};
