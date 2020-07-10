import _, {reject} from "lodash";
import web3 from "~/plugins/web3";

const ethUtil = require("ethereumjs-util");
const sigUtil = require("eth-sig-util");
import {ToastProgrammatic as Toast} from "buefy";

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
  set_status({commit}, payload) {
    commit("setStatus", payload);
  },
  set_address({commit}, payload) {
    commit("setAddress", payload);
  },
  async signAddress({rootGetters, commit}) {
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
          commit("setSignedAddresses", signature, {root: true});
          const signedAddresses = rootGetters.user.signed_addresses;
          this.$axios
            .put("/account/user/", {
              signed_addresses: signedAddresses
            })
            .then(() => {
              Toast.open({message: "Address signed!", type: "is-success"});
            })
            .catch(() => {
              Toast.open({
                message: "Something went wrong!",
                type: "is-danger"
              });
            });
        } else {
          Toast.open({message: "Signing failed!", type: "is-danger"});
        }
      }
    );
  },
  async createSignature({dispatch}, data) {
    const msgParams = [
      {
        type: "string",
        name: "Message",
        value: "Please provide a signature for your wallet"
      },
      {
        type: "address",
        name: "Address",
        value: data.address
      }
    ];

    const from = data.address;
    const params = [msgParams, from];
    const method = "eth_signTypedData";

    return new Promise((resolve, reject) => web3.currentProvider.sendAsync(
      {
        method,
        params,
        from
      },
      (err, result) => {

        if(err) {
          reject(err)
        }

        const recovered = sigUtil.recoverTypedSignatureLegacy({
          data: msgParams,
          sig: result.result
        });

        if (ethUtil.toChecksumAddress(recovered) === ethUtil.toChecksumAddress(from)) {
          this.$axios.post(`/account/eth-address/`, {
            address: data.address,
            signature: result.result
          })
          .then(async () => {
            Toast.open({
              message: this.$i18n.t('wallet.address_added'),
              type: "is-primary"
            });
            resolve(true)
            await dispatch("getUser", null, {root: true});
          })
          .catch(_ => {
            Toast.open({
              message: this.$i18n.t('wallet.address_failed_to_add'),
              type: "is-danger",
              duration: 6000
            });
            reject('failed to save')
          });
        }
      }
    ))
  }
};
