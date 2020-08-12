<template lang="pug">
  div.invoice-modal
    div.title.is-5.main-title Multisignature transaction
    div {{rawTransactionData}}
    div {{rawSignatureData}}
    div {{rawSignedTransaction}}
    div Invoice ID: {{invoice_id}}
</template>

<script>
import {createTransaction} from "~/plugins/bitcoreFunctions"

export default {
  name: "ModalBitcore",
  props: ["invoice_id"],
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
      this.$axios.get(`/admin/invoices/${this.invoice_id}/multisig`).then(resp => {
        let data = resp.data
        try {
          let {rawTransactionData, rawSignatureData} = createTransaction(
            data.cosig_1_wif, data.cosig_2_pub, data.spendables, data.payables, data.fee
          )
          this.rawSignatureData = rawSignatureData;
          this.rawTransactionData = rawTransactionData;
        } catch (e) {
          this.$buefy.toast.open({type: "is-danger", message: `Error: ${e}`})
        }
      }).catch(resp => {
        resp.response.data.map(i => this.$buefy.toast.open({type: "is-danger", message: `Error: ${i.message}`}))
      })
    },
    async sendRawTransaction() {
      let data = {transaction_hash: this.rawSignedTransaction}
      this.$axios.post(`/admin/invoices/${this.invoice_id}/multisig`, data).then(resp => {
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
