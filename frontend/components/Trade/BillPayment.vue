<template lang="pug">
  div
    h3.text-large.has-text-weight-bold Bill payment
    div.mt-2
      div.is-flex.align-items-center
        img(src="@/assets/images/bitcoin.svg").mr-2
        div.text-large Send 0.0205 BTC to 0x47FED2e47706EdEA3843dFc8985a16658c3b3d43
      div.is-flex.align-items-center.mt-2
        img(src="@/assets/images/logo_sm.png").mr-2
        div.text-large To accept 1 000 000 SIMBA
    div.trade-timer 1:59:57

</template>

<script>
  export default {
    name: 'trade-bill-payment',
    data: () => ({
    })
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
