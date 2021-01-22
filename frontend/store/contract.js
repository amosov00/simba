import web3 from "~/plugins/web3";
import {ToastProgrammatic as Toast} from 'buefy'

export const state = () => ({
  simba: {},
  simbaBalance: 0,
  sstBalance: 0,
  providerWSLink: "",
  providerHTTPLink: "",
});
export const getters = {
  SIMBA: s => s.simba,
  simbaBalance: s => s.simbaBalance,
  sstBalance: s => s.sstBalance,
  providerWSLink: s => s.providerWSLink,
  providerHTTPLink: s => s.providerHTTPLink,
};
export const mutations = {
  setContract: (state, payload) => (state.simba = payload),
  setSimbaBalance: (state, payload) => (state.simbaBalance = payload),
  setSstBalance: (state, payload) => (state.sstBalance = payload),
  setProviderWSLink: (state, payload) => (state.providerWSLink = payload),
  setProviderHTTPLink: (state, payload) => (state.providerHTTPLink = payload),
};
export const actions = {
  async fetchContractMeta({commit}) {
    const {data} = await this.$axios.get("/meta/eth/contract/");
    commit("setContract", data.contract);
    commit("setProviderWSLink", data.provider_ws_link);
    commit("setProviderHTTPLink", data.provider_http_link);
    return true;
  },

  transferSimbaToken({}, data) {
    const methodABI = this.$contract().SIMBA._jsonInterface.find(
      el => el.name === "transfer"
    );
    const amount = (data.amount * 1) + 5000
    const methodInputs = [data.address, amount];
    return new Promise((resolve, reject) => {
      ethereum.sendAsync(
        {
          method: "eth_sendTransaction",
          params: [
            {
              from: ethereum.selectedAddress,
              to: this.$contract().SIMBA._address,
              value: "0x00",
              gasPrice: web3.utils.toHex(web3.utils.toWei("24", "gwei")),
              gas: web3.utils.toHex("250000"),
              data: web3.eth.abi.encodeFunctionCall(
                methodABI,
                methodInputs
              )
            }
          ]
        },
        (err, result) => {
          if (result.result) {
            Toast.open({
              message: this.$i18n.t('wallet.transaction_success'),
              type: 'is-primary'
            })
            resolve(true)
          } else {
            Toast.open({
              message: this.$i18n.t('wallet.transaction_failed'),
              type: 'is-danger'
            })
            reject(false)
          }
        }
      )
    })
  },

  async fetchSimbaBalance({rootGetters, commit}) {
    let address = null
    if (window?.ethereum) {
      address = window.ethereum.selectedAddress;
    } else {
      const user = rootGetters["user"];
      if (user && user.user_eth_addresses.length > 0) {
        address = user.user_eth_addresses[0].address
      }
    }
    if (!address) {
      console.error("failed to fetch balance: no address found")
      return
    }
    this.$contract().SIMBA.methods.balanceOf(address)
      .call()
      .then(res => {
        commit("setSimbaBalance", res)
      })
      .catch(err => {
        console.error(err)
      })
  }
};
