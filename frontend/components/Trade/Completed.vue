<template lang="pug">
  div
    div.has-text-success.is-size-5.has-text-weight-bold {{$t('exchange.success')}}
    div.mt-4(v-if="isBuyInvoice")
      div.is-size-5
        span.has-text-weight-bold {{ numberWithCommas(invoice.simba_amount_proceeded) }} SIMBA
        =' '
        span.has-text-grey-light {{$t('exchange.issued')}}
      div.is-size-6
        div.mt-2 {{$t('exchange.wallet')}}:
          =' '
          a(:href="getBlockchainLink(invoice.target_eth_address, 'address', 'eth')" target="_blank").link {{ invoice.target_eth_address }}
        div.mt-2 {{$t('exchange.transaction_hash')}}:
          =' '
          a(:href="getBlockchainLink(issueTxHash, 'tx', 'eth')" target="_blank").link {{ issueTxHash }}
    div.mt-4(v-else)
      div.is-size-5
        span.has-text-weight-bold {{ btcFormat(invoice.btc_amount_proceeded) }} BTC
      div.is-size-6
        div.mt-2 {{$t('exchange.wallet')}}:
          =' '
          a(:href="getBlockchainLink(invoice.target_btc_address, 'address', 'btc')" target="_blank").link {{ invoice.target_btc_address }}
        div.mt-2 {{$t('exchange.transaction_hash')}}:
          =' '
          a(:href="getBlockchainLink(btcTxHash, 'tx', 'btc')" target="_blank").link {{ btcTxHash }}
        div.mt-2 {{$t('exchange.simba_redemption')}}:
          =' '
          a(:href="getBlockchainLink(redeemTxHash, 'tx', 'eth')" target="_blank").link {{ redeemTxHash }}
    div.mt-4
      a(href="/exchange/buysell?op=buy" v-if="isBuyInvoice").btn {{$t('exchange.buy_more')}}
      a(href="/exchange/buysell?op=sell" v-else).btn {{$t('exchange.sell_more')}}
</template>

<script>
import _ from 'lodash'
import { mapGetters, mapState } from 'vuex'
import invoiceMixins from '~/mixins/invoiceMixins'
import formatCurrency from '~/mixins/formatCurrency'

export default {
  name: 'trade-completed',
  mixins: [invoiceMixins, formatCurrency],
  data: () => ({}),
  computed: {
    ...mapGetters('exchange', ['isBuyInvoice']),
    ...mapState('exchange', ['invoice', 'operation']),
    redeemTxHash() {
      let tx = this.invoiceEthTxRedeem(this.invoice)
      let txHash = tx ? tx.transactionHash : null
      return txHash || this.invoice.eth_tx_hashes[0]
    },
    issueTxHash() {
      let tx = this.invoiceEthTxIssue(this.invoice)
      let txHash = tx ? tx.transactionHash : null
      return txHash || this.invoice.eth_tx_hashes[0]
    },
    btcTxHash() {
      if (_.isEmpty(this.invoice)) {
        return ''
      }
      return this.invoice.btc_tx_hashes.length > 0 ? this.invoice.btc_tx_hashes[0] : ''
    },
  },
  methods: {
    numberWithCommas(x) {
      return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
    },
  },
}
</script>

<style lang="sass"></style>
