<template lang="pug">
  div.invoice-modal
    div.title.is-5.main-title Multisignature transaction
    div Invoice ID: {{invoiceId}}
    div {{rawTransactionData}}
    div {{rawSignatureData}}
    div {{rawSignedTransaction}}
</template>

<script>
import {createTransaction} from "~/plugins/bitcoreFunctions"

export default {
  name: "ModalBitcore",
  props: ["invoiceId"],
  data() {
    return {
      rawTransactionData: null,
      rawSignatureData: null,
      rawSignedTransaction: null,
    };
  },
  async mounted() {
    await this.fetchData()
  },
  methods: {
    async fetchData() {
      this.$axios.get(`/admin/invoices/${this.invoiceId}/multisig`).then(resp => {
        let data = resp.data
        try {
          let {rawTransactionData} = createTransaction(
            data.cosig_1_wif, data.cosig_2_pub, data.spendables, data.payables, data.fee, data.testnet
          )
          this.rawTransactionData = rawTransactionData;
          this.rawSignatureData = rawSignatureData;
        } catch (e) {
          console.log(e.valueOf())
          this.$buefy.toast.open({type: "is-danger", message: `${e}`})
        }
      }).catch(resp => {
        resp.response.data.map(i => this.$buefy.toast.open({type: "is-danger", message: `Error: ${i.message}`}))
      })
    },
    async sendRawTransaction() {
      let data = {transaction_hash: this.rawSignedTransaction}
      this.$axios.post(`/admin/invoices/${this.invoiceId}/multisig`, data).then(resp => {
        // TODO add updated invoice to store
      }).catch(resp => {
        resp.response.data.map(i => this.$buefy.toast.open({type: "is-danger", message: `Error: ${i.message}`}))
      })
    }
  },
}
</script>

<style lang="sass" scoped>
.invoice-modal
  background: #ffffff
  max-width: 647px
  padding: 40px 73px
  margin: auto
</style>
