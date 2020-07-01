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

  redeemSimbaToken({}, data) {
    const methodABI = this.$contract().SIMBA._jsonInterface.find(
      el => el.name === "redeem"
    );
    const amount = (300000 * 1)
    const methodInputs = [amount, 'test'];
    ethereum.sendAsync(
      {
        method: "eth_sendTransaction",
        params: [
          {
            from: ethereum.selectedAddress,
            to: '0x60E1BF648580AafbFf6c1bc122BB1AE6Be7C1352',
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
          Toast.open({message: 'Transaction sent!', type: 'is-success'})
        } else {
          Toast.open({message: 'Transaction failed!', type: 'is-danger'})
        }
      }
    );
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
          Toast.open({message: 'Transaction sent!', type: 'is-success'})
        } else {
          Toast.open({message: 'Transaction failed!', type: 'is-danger'})
        }
      }
    );
  }
};