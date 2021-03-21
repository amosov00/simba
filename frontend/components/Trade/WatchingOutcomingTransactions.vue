<template lang="pug">
  div
    div.position-relative
      h3.text-large.has-text-weight-bold {{$t('exchange.status')}}
      div(v-if="isBuyInvoice")
        div.mt-3.is-size-6
          span.has-text-weight-bold {{ simbaFormat(invoice.simba_amount_proceeded) }} SIMBA
          span.has-text-grey-light  {{ ' ' + $t('exchange.sent_payment_simba') }}
        div.mt-2 {{$t('exchange.transaction_hash')}}:
          =' '
          a(:href="getBlockchainLink(ethIssueHash, 'tx', 'eth')" target="_blank").link {{ ethIssueHash }}
        div.mt-2 {{$t('exchange.wallet')}}:
          =' '
          a(:href="getBlockchainLink(invoice.target_eth_address, 'address', 'eth')" target="_blank").link {{ invoice.target_eth_address }}
        div.mt-2
          div {{$t('exchange.confirms')}} {{ETHTxConfirmations}}/{{minConfirmes}}

      div(v-else)
        div.mt-3.is-size-6 {{$t('exchange.sent_payment')}} {{ btcFormat(invoice.btc_amount_proceeded, 8) }} BTC
        div.mt-2 {{$t('exchange.transaction_hash')}}:
          =' '
          a(:href="getBlockchainLink(btcHash, 'tx', 'btc')" target="_blank").link {{ btcHash }}
        div.mt-2
          div {{$t('exchange.confirms')}} {{BTCTxConfirmations}}/{{minConfirmes}}


      b-loading(:active.sync="loading" :is-full-page="false")

</template>

<script>
import { mapActions, mapGetters, mapMutations, mapState } from 'vuex'

import invoiceMixins from '~/mixins/invoiceMixins'
import formatCurrency from '~/mixins/formatCurrency'

export default {
  name: 'trade-watching-outcoming-transactions',
  mixins: [invoiceMixins, formatCurrency],

  props: {
    loading: Boolean,
  },

  data: () => ({
    interval: null,
    tx_hash: '',
    received_payment_amount: 0,
    min_confirms: 3,
    currentConfirms: 0,
  }),

  computed: {
    ...mapGetters('exchange', ['isBuyInvoice']),
    ...mapState('exchange', ['invoice', 'invoiceId', 'operation', 'adminEthHash']),
    btcHash() {
      return this.invoice.btc_tx_hashes.length > 0 ? this.invoice.btc_tx_hashes[0] : ''
    },
    ethIssueHash() {
      let tx = this.invoiceEthTxIssue(this.invoice)
      let txHash = tx ? tx.transactionHash : null
      return txHash || this.invoice.eth_tx_hashes[0]
    },
    minConfirmes() {
      return this.$config.isProduction ? 3 : 1
    },
    ETHTxConfirmations() {
      let tx = this.invoiceEthTxTransfer(this.invoice)
      return tx ? tx.confirmations : 0
    },
    BTCTxConfirmations() {
      return this.invoice.btc_txs.length > 0 ? this.invoice.btc_txs[0].confirmations : 0
    },
  },
}
</script>

<style lang="sass"></style>
