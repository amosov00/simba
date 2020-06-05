<template lang="pug">
  div
    h3.text-large.has-text-weight-bold Confirm wallet
    div.is-flex.mt-2.align-items-center.space-between
      div.is-flex.align-items-center
        img(src="~assets/images/eth.svg").mr-2
        div.text-large {{ eth_wallet }}
      button.btn Confirm
</template>

<script>
  export default {
    name: 'trade-wallet-confirm',
    data: () => ({
      eth_wallet: "0x47FED2e47706EdEA3843dFc8985a16658c3b3d43"
    })
  }
</script>

<style lang="sass">
</style>
