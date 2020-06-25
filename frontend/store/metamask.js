import _ from "lodash";
import web3 from "~/plugins/web3";
const ethUtil = require("ethereumjs-util");
const sigUtil = require("eth-sig-util");
import { ToastProgrammatic as Toast } from "buefy";

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
  async signAddress({ rootGetters, commit }) {
    const msgParams = [
      {
        type: "string",
        name: "Message",
        value: "Please provide a signature for your wallet"
      },
      {
        type: "address",
        name: "Address",
        value: `${window.ethereum.selectedAddress}`
      }
    ];

    const from = window.ethereum.selectedAddress;
    const params = [msgParams, from];
    const method = "eth_signTypedData";

    web3.currentProvider.sendAsync(
      {
        method,
        params,
        from
      },
      (err, result) => {
        const recovered = sigUtil.recoverTypedSignatureLegacy({
          data: msgParams,
          sig: result.result
        });

        if (
          ethUtil.toChecksumAddress(recovered) ===
          ethUtil.toChecksumAddress(from)
        ) {
          const signature = {
            address: from,
            signature: result.result
          };
          commit("setSignedAddresses", signature, { root: true });
          const signedAddresses = rootGetters.user.signed_addresses;
          this.$axios
            .put("/account/user/", {
              signed_addresses: signedAddresses
            })
            .then(() => {
              Toast.open({ message: "Address signed!", type: "is-success" });
            })
            .catch(() => {
              Toast.open({
                message: "Something went wrong!",
                type: "is-danger"
              });
            });
        } else {
          Toast.open({ message: "Signing failed!", type: "is-danger" });
        }
      }
    );
  }
};
