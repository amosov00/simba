<template lang="pug">
  div
    h3.text-large.has-text-weight-bold Confirm wallet
    div.is-flex.mt-2.align-items-center.space-between
      div(v-if="multi_props.op !== 'sell'").is-flex.align-items-center
        img(src="~assets/images/eth.svg").mr-2
        div.text-large {{ eth_address }}
      div(v-else).is-flex.align-items-center
        img(src="~assets/images/bitcoin.svg").mr-2
        b-field
          b-input
        div
          button.btn(@click="testSell") Redeem (test)
      button.btn(@click="next") Confirm
</template>

<script>
  export default {
    name: 'trade-wallet-confirm',
    props: {
      multi_props: Object
    },

    data: () => ({
    }),

    computed: {
      eth_address() {
        return this.$store.getters['exchange/tradeData']['eth_address']
      }
    },
    methods: {
      async testSell() {
        await this.$store.dispatch('contract/fetchContract');
        this.$store.dispatch('contract/redeemSimbaToken', {});
      },
      next(){
        this.$parent.$emit('nextStep')
      }
    }
  }
</script>

<style lang="sass">
</style>
