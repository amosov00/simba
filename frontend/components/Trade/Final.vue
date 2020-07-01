<template lang="pug">
  div
    div.has-text-success.is-size-5.has-text-weight-bold Success!
    div.mt-4
      div.is-size-5
        span.has-text-weight-bold {{ numberWithCommas(multi_props.buy_info.simba_issued-50000) }} SIMBA
        =' '
        span.has-text-grey-light issued
      div.is-size-6
        div.mt-2 Wallet:
          =' '
          a(:href="'https://etherscan.io/address/' + multi_props.buy_info.target_eth" target="_blank").link {{ multi_props.buy_info.target_eth }}
        div.mt-2 Simba token txHash:
          =' '
          a(:href="'https://etherscan.io/tx/' + multi_props.buy_info.tx_hash" target="_blank").link {{ multi_props.buy_info.tx_hash }}
    div.mt-4
      a(href="/exchange/buysell?op=buy").btn Buy more
</template>

<script>
  export default {
    name: 'trade-final',
    props: {
      multi_props: Object
    },
    data: () => ({
    }),
    methods: {
      numberWithCommas(x) {
        return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
      },
    }
  }
</script>

<style lang="sass">
</style>
