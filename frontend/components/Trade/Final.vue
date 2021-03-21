<template lang="pug">
  div
    div.has-text-success.is-size-5.has-text-weight-bold {{$t('exchange.success')}}
    div.mt-4(v-if="isBuyInvoice")
      div.is-size-5
        span.has-text-weight-bold {{ numberWithCommas(tradeData.simba_issued - 50000) }} SIMBA
        =' '
        span.has-text-grey-light {{$t('exchange.issued')}}
      div.is-size-6
        div.mt-2 {{$t('exchange.wallet')}}:
          =' '
          a(:href="getBlockchainLink(tradeData.target_eth, 'address', 'eth')" target="_blank").link {{ tradeData.target_eth }}
        div.mt-2 Simba token txHash:
          =' '
          a(:href="getBlockchainLink(issueTxHash, 'tx', 'eth')" target="_blank").link {{ issueTxHash }}
    div.mt-4(v-else)
      div.is-size-5
        span.has-text-weight-bold {{ convert(tradeData.simba_issued) }} BTC
      div.is-size-6
        div.mt-2 {{$t('exchange.wallet')}}:
          =' '
          a(:href="getBlockchainLink(tradeData.btc_redeem_wallet, 'address', 'btc')" target="_blank").link {{ tradeData.btc_redeem_wallet }}
        div.mt-2 {{$t('exchange.transaction_hash')}}:
          =' '
          a(:href="getBlockchainLink(tradeData.tx_hash, 'tx', 'btc')" target="_blank").link {{ tradeData.tx_hash }}
        div.mt-2 {{$t('exchange.simba_redemption')}}:
          =' '
          a(:href="getBlockchainLink(redeemTxHash, 'tx', 'eth')" target="_blank").link {{ redeemTxHash }}
    div.mt-4
      a(href="/exchange/buysell?op=buy" v-if="isBuyInvoice").btn {{$t('exchange.buy_more')}}
      a(href="/exchange/buysell?op=sell" v-else).btn {{$t('exchange.sell_more')}}
</template>

<script>
import { mapGetters } from 'vuex'
import invoiceMixins from '~/mixins/invoiceMixins'

export default {
  name: 'trade-final',
  mixins: [invoiceMixins],
  data: () => ({}),
  computed: {
    ...mapGetters('exchange', ['tradeData']),
    redeemTxHash() {
      let tx = this.$store.getters['exchange/ethTxByEvent']('OnRedeemed')
      return tx ? tx.transactionHash : ''
    },
    issueTxHash() {
      let tx = this.$store.getters['exchange/ethTxByEvent']('OnIssued')
      return tx ? tx.transactionHash : ''
    },
    isBuy() {
      return this.tradeData.operation === 1
    },
  },
  methods: {
    numberWithCommas(x) {
      return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
    },
    convert(simba) {
      let test = (simba / 100000000).toFixed(4)

      if (isNaN(test)) {
        return 0
      }

      return parseFloat(test)
    },
  },
}
</script>

<style lang="sass"></style>
