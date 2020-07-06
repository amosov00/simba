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
      b-button.btn(@click="confirm" :loading="btn_loading") {{$t('exchange.create')}}
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

    data: () => ({
      isConverting: false,
      error: false,
      btc: 0.00200000,
      simba: 200000,
      btn_loading: false,
      money: {
        thousands: ' ',
        precision: 0,
        masked: false
      },
      invoice_id: '',
      check_btc_address_interval: null
    }),

    computed: {
      isBuy() {
        return this.$store.getters['exchange/tradeData']['operation'] === 1
      },

      tradeData() {
        return this.$store.getters['exchange/tradeData']
      }
    },

    methods: {
      async checkBitcoinAddress(id) {
        return await this.$store.dispatch('invoices/fetchSingle', id)
      },

      async confirm() {

        if(this.btc < 0.002 || this.simba < 200000) {
          this.error = true
          return
        }

        this.btn_loading = true;
        this.$store.commit('exchange/setTradeData', { prop: 'simba', value: this.simba })
        this.$store.commit('exchange/setTradeData', { prop: 'btc', value: this.btc })

        // create transaction
        let created_invoice = await this.$store.dispatch('invoices/createTransaction', this.tradeData.operation);

        this.$store.commit('exchange/setTradeData', {prop: 'invoice_id', value: created_invoice._id})

        this.check_btc_address_interval = setInterval(async () => {
          let invoice = await this.checkBitcoinAddress(created_invoice._id)

          if(invoice.target_btc_address) {
            clearInterval(this.check_btc_address_interval)
            this.btn_loading = false
            let data_for_update = { id: created_invoice._id, eth_address: this.tradeData.eth_address, simba_amount: this.tradeData.simba}

            // Update invoice with amounts
            let updated_invoice_res = await this.$store.dispatch('invoices/updateTransaction', data_for_update)

            // Add invoice id to url, go to next step
            if(updated_invoice_res) {
              this.$nuxt.$router.push({ path: '/exchange/buysell', query: {id: invoice._id }})
              //this.$parent.$emit('nextStep')
            }
          }

        }, 3000)
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
