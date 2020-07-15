export default {
  methods: {
    findEthTransactionByEvent(invoice, eventName) {
      return invoice.eth_txs.find((el) => {
        return el.event === eventName
      })
    }
  }
}
