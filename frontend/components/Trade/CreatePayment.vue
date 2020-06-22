<template lang="pug">
  div
    h3.text-large.has-text-weight-bold Create payment bill
    div.is-flex.mt-2.align-items-center.space-between
      div.is-flex.align-items-center
        div.is-flex.flex-column.align-items-center.smb-input-wrapper
          money(v-model="simba" v-bind="money" v-on:input="convert").smb-input
          //- input(v-model="simba" type="text" v-money="money" v-on:input="convert").smb-input
        span.mr-2.ml-2
          | =
        div.is-flex.flex-column.align-items-center.smb-input-wrapper
          input(v-model="btc" type="text" v-on:input="convertBTCtoSimba").smb-input
      button.btn(@click="confirm") Confirm
    div.is-flex.has-text-centered
      div.smb-input-wrapper.mr-4.mt-2 SIMBA
      div.smb-input-wrapper.mt-2 BTC
    div(v-if="errors").error.has-text-danger.mt-4 {{ errors[0] }}
</template>

<script>
  import {Money} from 'v-money'

  export default {
    name: 'trade-create-payment',

    components: {Money},

    data: () => ({
      errors: [],
      btc: 0.00200000,
      simba: 200000,
      money: {
        thousands: ' ',
        precision: 0,
        masked: false /* doesn't work with directive */
      }
    }),
    methods: {
      confirm() {

        if(this.btc < 0.002 || this.simba < 200000) {
          this.errors.push('Minimum amount 200,000 SIMBA')
          return
        }

        this.$store.commit('exchange/setTradeData', { prop: 'simba', value: this.simba })
        this.$store.commit('exchange/setTradeData', { prop: 'btc', value: this.btc })

        this.$parent.$emit('nextStep')
      },

      convert() {

        let test = (this.simba/100000000).toFixed(4);

        if(isNaN(test)) {
          this.btc = 0
        } else {
          this.btc = test;
        }
      },

      convertBTCtoSimba() {
        let test = (this.btc*100000000).toFixed(0);

        if(isNaN(test)) {
          this.simba = 0
        } else {
          this.simba = test;
        }
      }
    }
  }
</script>

<style lang="sass">
</style>
