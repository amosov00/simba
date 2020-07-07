import _, { stubArray } from "lodash";
import { ToastProgrammatic as Toast, DialogProgrammatic as Dialog } from "buefy";

export const state = () => ({
  user: null,
  contract: "",
  tradeData: {
    operation: 1,
    eth_address: "",
    simba: 0,
    btc: 0
  },
  loginDataBuffer: {}
});

export const getters = {
  user: s => s.user,
  contract: s => s.contract,
  tradeData: s => s.tradeData,
  loginDataBuffer: s => s.loginDataBuffer
};

export const mutations = {
  setUser: (state, user) => (state.user = user),
  deleteUser: state => (state.user = null),
  setContract: (state, data) => (state.contract = data),
  setTradeData: (state, payload) => {
    state.tradeData[payload.prop] = payload.value;
  },
  setTwoFactor: (state, payload) => (state.user.two_factor = payload),
  setSignedAddresses: (state, payload) =>
    state.user.signed_addresses.push(payload),
  setLoginDataBuffer: (state, payload) => {
    state.loginDataBuffer = payload
  }
};

export const actions = {
  async fetchReferrals() {
    return await this.$axios
      .get("/account/referrals/")
      .then(res => res.data["referrals"])
      .catch(() => false);
  },

  async changeAddresses({}, data) {
    return await this.$axios
      .put("/account/user/", data)
      .then(() => true)
      .catch(() => false);
  },

  async fetchContracts({ commit }) {
    return await this.$axios
      .get("/meta/eth/contract/")
      .then(res => {
        commit("setContract", res.data);
        return true;
      })
      .catch(_ => false);
  },

  async activateAccount({}, data) {
    if (!data) return false;

    return await this.$axios
      .post("/account/verify/", data)
      .then(resp => {
        return true;
      })
      .catch(_ => {
        return false;
      });
  },

  async getUser({ commit }) {
    return await this.$axios
      .get("/account/user/")
      .then(resp => {
        if (resp.status === 200) {
          commit("setUser", resp.data);
          return true;
        }

        return false;
      })
      .catch(_ => false);
  },

  async fetchRefLink({}) {
    return await this.$axios
      .get("/account/referral_link/")
      .then(resp => {
        if (resp.status === 200) {
          return resp.data;
        }
        return false;
      })
      .catch(_ => false);
  },

  async signUp({ commit }, data) {
    if (!data) return false;
    return await this.$axios
      .post("/account/signup/", data)
      .then(resp => {
        Toast.open({
          message:
            this.$i18n.t('auth.sign_up_success'),
          type: "is-success",
          duration: 6000
        });
        return true;
      })
      .catch(resp => {

        if(resp.response.data[0].message === 'Referral link invalid') {
          Dialog.alert({
            message: `${this.$i18n.t('auth.sign_up_error_referral')} <a href='mailto:support@simba.storage'>${this.$i18n.t('auth.to_support')}</a>`,
            type: "is-primary",
          })
        } else {
          Toast.open({
            message: resp.response.data[0].message,
            type: "is-danger",
            duration: 6000
          })
        }
        return false;
      });
  },
  async changeProfile({}, data) {
    return await this.$axios
      .put("/account/user/", JSON.stringify(data))
      .then(_ => {
        return true;
      })
      .catch(err => {
        return false;
      });
  },
  async changePassword({}, data) {
    return await this.$axios
      .post("/account/change_password/", data)
      .then(_ => {
        return true;
      })
      .catch(err => {
        return false;
      });
  },
  async startRecover({}, data) {
    return await this.$axios
      .post("/account/recover/", data)
      .then(_ => {
        return true;
      })
      .catch(err => {
        return false;
      });
  },
  async finishRecover({}, data) {
    return await this.$axios
      .put("/account/recover/", data)
      .then(_ => {
        return true;
      })
      .catch(err => {
        return false;
      });
  },
  async confirm2fa({ commit }, data) {
    return await this.$axios
      .post("/account/2fa/", {
        token: data.token,
        pin_code: data.pin_code
      })
      .then(() => {
        commit("setTwoFactor", true);
        Toast.open({ message: this.$i18n.t('messages.two_factor_enable_success'), type: "is-primary" });
      })
      .catch(() => {
        Toast.open({ message: this.$i18n.t('messages.two_factor_enable_failed'), type: "is-danger" });
      });
  },
  async delete2fa({ commit }, pin_code) {
    return await this.$axios
      .delete("/account/2fa/", {
        data: {
          pin_code: `${pin_code}`
        }
      })
      .then(() => {
        commit("setTwoFactor", false);
        Toast.open({
          message: this.$i18n.t('messages.two_factor_disable_success'),
          type: "is-primary"
        });
      })
      .catch(() => {
        Toast.open({ message: this.$i18n.t('messages.two_factor_disable_failed'), type: "is-danger" });
      });
  }
};
