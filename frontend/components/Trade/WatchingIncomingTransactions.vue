<template lang="pug">
  div
    div.position-relative
      h3.text-large.has-text-weight-bold {{$t('exchange.status')}}
      div(v-if="isBuyInvoice")
        div.mt-3.is-size-6 {{$t('exchange.received_payment')}} {{ btcFormat(btcAmount, 8) }} BTC
        div.mt-2 {{$t('exchange.transaction_hash')}}:
          =' '
          a(:href="getBlockchainLink(btcHash, 'tx', 'btc')" target="_blank").link {{ btcHash }}
        div.mt-2
          div {{$t('exchange.confirms')}} {{BTCTxConfirmations}}/{{minConfirmes}}
        div.mt-4
          div {{$t('exchange.verify_auto')}}
          div {{$t('exchange.payment_confirmation_buy')}}

      div(v-else)
        div(v-if="invoice.eth_txs.length > 0 && invoice.btc_txs.length === 0")
          div.mt-3.is-size-6 {{$t('exchange.received_payment')}} {{ simbaFormat(invoice.simba_amount_proceeded) }} SIMBA
          div.mt-2 {{$t('exchange.transaction_hash')}}:
            =' '
            a(:href="getBlockchainLink(ethTransferHash, 'tx', 'eth')" target="_blank").link {{ ethTransferHash }}
          div.mt-2
            div {{$t('exchange.confirms')}} {{ETHTxConfirmations}}/{{minConfirmes}}

        div(v-else)
          div.mt-3.is-size-6 {{$t('exchange.sent_payment')}} {{ btcFormat(btcAmount, 8) }} BTC
          div.mt-2 {{$t('exchange.transaction_hash')}}:
            =' '
            a(:href="getBlockchainLink(btcHash, 'tx', 'btc')" target="_blank").link {{ btcHash }}
          div.mt-2
            div {{$t('exchange.confirms')}} {{BTCTxConfirmations}}/{{minConfirmes}}

        div.mt-4
          div {{$t('exchange.verify_auto')}}
          div {{$t('exchange.payment_confirmation_sell')}}

      b-loading(:active.sync="loading" :is-full-page="false")

</template>

<script>
import { mapActions, mapGetters, mapMutations, mapState } from 'vuex'

import invoiceMixins from '~/mixins/invoiceMixins'
import formatCurrency from '~/mixins/formatCurrency'

export default {
  name: 'trade-watching-transactions',
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
      let hash = this.invoice.btc_tx_hashes.length > 0 ? this.invoice.btc_tx_hashes[0] : ''
      if (!hash) {
        hash = this.invoiceBTCHash(this.invoice)
      }
      return hash
    },
    btcAmount() {
      return this.invoice.btc_amount_proceeded || this.invoiceBTCAmount(this.invoice)
    },
    ethTransferHash() {
      let tx = this.invoiceEthTxTransfer(this.invoice)
      let txHash = tx ? tx.transactionHash : null
      return txHash || this.invoice.eth_tx_hashes[0]
    },
    ethAmount() {
      return this.invoice.eth_amount_proceeded
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
