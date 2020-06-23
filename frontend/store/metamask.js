import _ from "lodash";
import web3 from "~/plugins/web3";
import { ToastProgrammatic as Toast } from 'buefy'

export const state = () => ({
  status: "offline",
  address: ""
});

export const getters = {
  status: s => s.status,
  address: s => s.address
};

export const mutations = {
  setStatus: (state, data) => (state.status = data),
  setAddress: (state, data) => (state.address = data)
};

export const actions = {
  set_status({ commit }, payload) {
    commit("setStatus", payload);
  },
  set_address({ commit }, payload) {
    commit("setAddress", payload);
  },
  signAddress({ commit }, address) {
    console.log(address)
    ethereum.sendAsync(
      {
        method: "personal_sign",
        params: [
          {
            from: ethereum.selectedAddress,
            to: this.$contract().SIMBA._address,
            value: "0x00",
            gasPrice: web3.utils.toHex(web3.utils.toWei("24", "gwei")),
            gas: web3.utils.toHex("250000"),
            message: 'Sign'
          }
        ]
      },
      (err, result) => {
        if (result.result) {
          Toast.open({ message: "Transaction sent!", type: "is-success" });
        } else {
          Toast.open({ message: "Transaction failed!", type: "is-danger" });
        }
      }
    );
  }
};
