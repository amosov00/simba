import web3 from "~/plugins/web3";
import { ToastProgrammatic as Toast } from 'buefy'

export const state = () => ({
  SIMBA: {}
});
export const getters = {
  SIMBA: s => s.SIMBA
};
export const mutations = {
  setContract: (state, payload) => (state.SIMBA = payload)
};
export const actions = {
  async fetchContract({ commit }) {
    const { data } = await this.$axios.get("/meta/eth/contract/");
    commit("setContract", data);
    return true;
  },

  transferSimbaToken({}, data) {
    const methodABI = this.$contract().SIMBA._jsonInterface.find(
      el => el.name === "transfer"
    );
    const amount = (data.amount * 1) + 5000
    const methodInputs = [data.address, amount];
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
          Toast.open({message: this.$i18n.t('wallet.transaction_success'), type: 'is-primary'})
        } else {
          Toast.open({message: this.$i18n.t('wallet.transaction_failed'), type: 'is-danger'})
        }
      }
    );
  }
};
