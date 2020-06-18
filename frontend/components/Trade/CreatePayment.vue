<template lang="pug">
  div
    h3.text-large.has-text-weight-bold Create payment bill
    div.is-flex.mt-2.align-items-center.space-between
      div.is-flex.align-items-center
        div.is-flex.flex-column.align-items-center.smb-input-wrapper
          input(v-model="simba" type="text" v-on:input="convert").smb-input
        span.mr-2.ml-2
          | =
        div.is-flex.flex-column.align-items-center.smb-input-wrapper
          input(v-model="btc" type="text").smb-input
      button.btn(@click="confirm") Confirm
    div.is-flex.has-text-centered
      div.smb-input-wrapper.mr-4.mt-2 SIMBA
      div.smb-input-wrapper.mt-2 BTC
    div.error.has-text-danger.mt-4 Minimum amount 200 000
</template>

<script>
  export default {
    name: 'trade-create-payment',
    data: () => ({
      btc: 0,
      simba: 0
    }),
    methods: {
      confirm() {
        this.$store.commit('setTradeData', {
          simba: this.simba,
          btc: this.btc
        })

        this.$parent.$emit('nextStep')
      },

      convert() {
        let test = (this.simba/100000000).toFixed(8);

        if(isNaN(test)) {
          this.btc = 0
        } else {
          this.btc = test;
        }

      }
    }
  }
</script>

<style lang="sass">
</style>
