<template lang="pug">
  div
    div.has-text-success.is-size-5.has-text-weight-bold {{$t('exchange.success')}}
    div.mt-4(v-if="isBuy")
      div.is-size-5
        span.has-text-weight-bold {{ numberWithCommas(tradeData.simba_issued) }} SIMBA
        =' '
        span.has-text-grey-light {{$t('exchange.issued')}}
      div.is-size-6
        div.mt-2 {{$t('exchange.wallet')}}:
          =' '
          a(:href="'https://etherscan.io/address/' + tradeData.target_eth" target="_blank").link {{ tradeData.target_eth }}
        div.mt-2 Simba token txHash:
          =' '
          a(:href="'https://etherscan.io/tx/' + tradeData.tx_hash" target="_blank").link {{ tradeData.tx_hash }}
    div.mt-4(v-else)
      div.is-size-5
        span.has-text-weight-bold {{ convert(tradeData.simba_issued) }} BTC
      div.is-size-6
        div.mt-2 {{$t('exchange.wallet')}}:
          =' '
          a(:href="'https://live.blockcypher.com/btc-testnet/address/' + tradeData.btc_redeem_wallet" target="_blank").link {{ tradeData.btc_redeem_wallet }}
        div.mt-2 {{$t('exchange.transaction_hash')}}:
          =' '
          a(:href="'https://live.blockcypher.com/btc-testnet/tx/' + tradeData.tx_hash" target="_blank").link {{ tradeData.tx_hash }}
        div.mt-2 Simba redemption:
          =' '
          a(:href="'https://etherscan.io/tx/' + tradeData.tx_hash_redeem" target="_blank").link {{ tradeData.tx_hash_redeem }}
    div.mt-4
      a(href="/exchange/buysell?op=buy" v-if="isBuy").btn {{$t('exchange.buy_more')}}
      a(href="/exchange/buysell?op=sell" v-else).btn {{$t('exchange.sell_more')}}
</template>

<script>

  export default {
    name: 'trade-final',
    data: () => ({
    }),
    computed: {
      tradeData() {
        return this.$store.getters['exchange/tradeData'];
      },
      isBuy() {
        return this.$store.getters['exchange/tradeData']['operation'] === 1
      },
    },
    methods: {
      numberWithCommas(x) {
        return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
      },
      convert(simba) {

        let test = (simba/100000000).toFixed(4);

        if(isNaN(test)) {
          return 0
        }

        return test
      }
    }
  }
</script>

<style lang="sass">
</style>
