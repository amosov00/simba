<template lang="pug">
  div
    h3.text-large.has-text-weight-bold Bill payment
    div.mt-2
      div.is-flex.align-items-center
        img(src="@/assets/images/bitcoin.svg").mr-2
        div.text-large Send {{ tradeData.btc }} BTC to {{ btc_address }}
      div.is-flex.align-items-center.mt-2
        img(src="@/assets/images/logo_sm.png").mr-2
        div.text-large To accept {{ tradeData.simba }} SIMBA
    div.trade-timer 1:59:57

</template>

<script>
  export default {
    name: 'trade-bill-payment',
    computed: {
      btc_address() {
        return '0x' + this.$store.getters.btc_address.toUpperCase();
      },
      tradeData() {
        return this.$store.getters.tradeData;
      }
    },
    data: () => ({
    }),
    async mounted() {
      await this.$store.dispatch('getBtcAddress')
    }
  }
</script>

<style lang="sass" scoped>
  .trade-timer
    margin-top: 50px
    font-style: normal
    font-weight: 100
    font-size: 36px
    line-height: 100%
    color: #000000
</style>
