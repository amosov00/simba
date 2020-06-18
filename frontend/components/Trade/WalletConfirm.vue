<template lang="pug">
  div
    h3.text-large.has-text-weight-bold Confirm wallet
    div.is-flex.mt-2.align-items-center.space-between
      div.is-flex.align-items-center
        img(src="~assets/images/eth.svg").mr-2
        div.text-large {{ metamask_wallet_address }}
      button.btn(@click="next") Confirm
</template>

<script>
  export default {
    name: 'trade-wallet-confirm',
    data: () => ({
      eth_wallet: ""
    }),
    computed: {
      metamask_wallet_address() {
        return this.$store.getters['metamask/address']
      }
    },
    methods: {
      next(){
        this.$parent.$emit('nextStep')
      }
    }
  }
</script>

<style lang="sass">
</style>
