<template lang="pug">
  div
    div.has-text-success.is-size-5.has-text-weight-bold {{$t('exchange.success')}}
    div.mt-4
      div.is-size-5
        span.has-text-weight-bold {{ numberWithCommas(tradeData.simba_issued-50000) }} SIMBA
        =' '
        span.has-text-grey-light {{$t('exchange.issued')}}
      div.is-size-6
        div.mt-2 {{$t('exchange.wallet')}}:
          =' '
          a(:href="'https://etherscan.io/address/' + tradeData.target_eth" target="_blank").link {{ tradeData.target_eth }}
        div.mt-2 Simba token txHash:
          =' '
          a(:href="'https://etherscan.io/tx/' + tradeData.tx_hash" target="_blank").link {{ tradeData.tx_hash }}
    div.mt-4
      a(href="/exchange/buysell?op=buy").btn {{$t('exchange.buy_more')}}
</template>

<script>
  export default {
    name: 'trade-final',
    data: () => ({
    }),
    computed: {
      tradeData() {
        return this.$store.getters['exchange/tradeData'];
      }
    },
    methods: {
      numberWithCommas(x) {
        return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
      },
    }
  }
</script>

<style lang="sass">
</style>
