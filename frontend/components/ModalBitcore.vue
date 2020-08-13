<template lang="pug">
  div.invoice-modal
    div.title.is-5.main-title Multisignature transaction
    h3 Invoice ID: {{invoice._id}}
    b-field(label="Transaction data")
      b-input(v-model="rawTransactionData" type="textarea" disabled)
    b-field(label="Signature data")
      b-input(v-model="rawSignatureData" type="textarea" disabled)
    b-field(label="Completed raw transaction")
      b-input(v-model="rawSignedTransaction" type="textarea")
    b-button(type="is-primary" @click="sendRawTransaction") Broadcast transaction
</template>

<script>

export default {
  name: "ModalBitcore",
  props: ["invoice"],
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
      this.$axios.get(`/admin/invoices/${this.invoice._id}/multisig`).then(resp => {
        this.rawTransactionData = resp.data.rawTransactionData;
        this.rawSignatureData = resp.data.rawSignatureData;
      }).catch(resp => {
        resp.response.data.map(i => this.$buefy.toast.open({type: "is-danger", message: `Error: ${i.message}`}))
      })
    },
    async sendRawTransaction() {
      let data = {transaction_hash: this.rawSignedTransaction}
      this.$axios.post(`/admin/invoices/${this.invoice._id}/multisig`, data).then(resp => {
        console.log(resp.data)
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
