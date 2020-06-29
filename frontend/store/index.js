import _, { stubArray } from "lodash";
import { ToastProgrammatic as Toast } from "buefy";

export const state = () => ({
  user: null,
  btc_address: "",
  contract: "",
  tradeData: {
    operation: 1,
    eth_address: "",
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
  setTradeData: (state, payload) => {
    state.tradeData[payload.prop] = payload.value;
  },
  setTwoFactor: (state, payload) => (state.user.two_factor = payload),
  setSignedAddresses: (state, payload) =>
    state.user.signed_addresses.push(payload)
};

export const actions = {
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

  async getBtcAddress({ commit }) {
    return await this.$axios
      .get("/account/btc-address/")
      .then(resp => {
        commit("setBtcAddress", resp.data.address);
        return true;
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
            "Successfully registered! Please check your email to activate your account.",
          type: "is-success",
          duration: "6000"
        });
        return true;
      })
      .catch(resp => {
        Toast.open({
          message: resp.response.data[0].message,
          type: "is-danger",
          duration: "6000"
        });
        return false;
      });
  },
  async changeProfile({}, data) {
    console.log(data);

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
        Toast.open({ message: "2FA successfuly enabled!", type: "is-success" });
      })
      .catch(() => {
        Toast.open({ message: "Something went wrong!", type: "is-danger" });
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
          message: "2FA successfuly disabled!",
          type: "is-success"
        });
      })
      .catch(() => {
        Toast.open({ message: "Something went wrong!", type: "is-danger" });
      });
  }
};
