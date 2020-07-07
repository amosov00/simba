<template lang="pug">
  div
    h3.text-large.has-text-weight-bold {{$t('exchange.cr_payment_bill')}}
    div.is-flex.mt-2.align-items-center.space-between
      div.is-flex.align-items-center(:class="{ 'flex-row-reverse': isBuy}")
        div.is-flex.flex-column.align-items-center.smb-input-wrapper
          //--money(v-model.lazy="simba" v-bind="money" change.native="convert").smb-input
          input(v-model="simba" type="text" @input="convert").smb-input
        span.mr-2.ml-2
          | =
        div.is-flex.flex-column.align-items-center.smb-input-wrapper
          input(v-model="btc" type="text" @input="convertBTCtoSimba($event)" maxlength="10").smb-input
      b-button.btn(@click="confirm") {{$t('exchange.create')}}
    div.is-flex.has-text-centered(:class="{ 'flex-row-reverse': isBuy, 'justify-content-end': isBuy}")
      div.smb-input-wrapper.mt-2 SIMBA
      span.mr-4
      div.smb-input-wrapper.mt-2 BTC
    div(v-if="error").error.has-text-danger.mt-4 {{ $t('exchange.amount_err') }} 200,000 SIMBA
</template>

<script>
  import {Money} from 'v-money'

  export default {
    name: 'trade-create-payment',

    components: {Money},

    props: {
      multi_props: Object
    },

    data: () => ({
      isConverting: false,
      error: false,
      btc: 0.00200000,
      simba: 200000,
      money: {
        thousands: ' ',
        precision: 0,
        masked: false
      },
      invoice_id: ''
    }),

    computed: {
      isBuy() {
        return this.multi_props.op === 'buy'
      },
    },

    methods: {
      async confirm() {

        if(this.btc < 0.002 || this.simba < 200000) {
          this.error = true
          return
        }

        this.$store.commit('exchange/setTradeData', { prop: 'simba', value: this.simba })
        this.$store.commit('exchange/setTradeData', { prop: 'btc', value: this.btc })

        this.$parent.$emit('nextStep')
      },

      convert() {
        if(this.isConverting) {
          return
        }

        let test = (this.simba/100000000).toFixed(8);

        if(isNaN(test)) {
          this.btc = 0
        } else {
          this.btc = test;
        }
      },

      convertBTCtoSimba(e) {
        this.isConverting = true
        //let test = (this.btc*100000000).toFixed(0);
        let test = e.target.value;

        if(isNaN(test)) {
          this.btc = 0
          this.simba = 0
        } else {
          this.btc = test;
          this.simba = (this.btc*100000000).toFixed(0)
        }

        this.isConverting = false
      }
    }
  }
</script>

<style lang="sass">
</style>
