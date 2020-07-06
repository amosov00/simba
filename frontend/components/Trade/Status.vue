<template lang="pug">
  div
    h3.text-large.has-text-weight-bold Status
    div.mt-3.is-size-6 Recivied payment {{ parseFloat(convert(multi_props.buy_info.btc_amount_proceeded)) }} BTC
    div.mt-2 Transaction hash:
      =' '
      a(:href="'https://etherscan.io/tx/' + multi_props.buy_info.tx_hash" target="_blank").link {{ multi_props.buy_info.tx_hash }}
    div.mt-2 Confirmation 1/3
</template>

<script>
  export default {
    name: 'trade-status',
    data: () => ({
    }),
    props: {
      multi_props: Object
    },
    methods: {
      convert(simba) {

        let test = (simba/100000000).toFixed(8);

        if(isNaN(test)) {
          return 0
        }

        return test
      },
    }
  }
</script>

<style lang="sass">
</style>
