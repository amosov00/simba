<template lang="pug">
  div
    h3.text-large.has-text-weight-bold {{$t('exchange.cr_payment_bill')}}
    div.is-flex.mt-2.align-items-center.space-between
      div.is-flex.align-items-center(:class="{ 'flex-row-reverse': isBuy}")
        div.is-flex.flex-column.align-items-center.smb-input-wrapper
          //--money(v-model.lazy="simba" v-bind="money" change.native="convert").smb-input
          input(v-model="simba" type="text" @input="convert" :disabled="btn_loading").smb-input
        span.mr-2.ml-2
          | =
        div.is-flex.flex-column.align-items-center.smb-input-wrapper
          input(v-model="btc" type="text" @input="convertBTCtoSimba($event)" maxlength="10" :disabled="btn_loading").smb-input
      b-button.btn(@click="confirm" :loading="btn_loading" :disabled="!accepted_terms") {{$t('exchange.create')}}
    div.is-flex.space-between
      div.is-flex.has-text-centered(:class="{ 'flex-row-reverse': isBuy, 'justify-content-end': isBuy}")
        div.smb-input-wrapper.mt-2 SIMBA
        span.mr-4
        div.smb-input-wrapper.mt-2 BTC
      div
        ValidationProvider(:rules="{ required: { allowFalse: false } }" v-slot="{ errors }" :name="$i18n.t('auth.terms_of_agreement')" tag="div").mt-2
          b-checkbox(v-model="accepted_terms" :disabled="btn_loading").checkbox-fix
            span {{$t('auth.i_accept')}}
            =' '
            a(href="https://simba.storage/terms-of-use.pdf" target="_blank" rel="noreferrer noopener").link {{$i18n.t('auth.terms_of_agreement')}}
          span.validaton-error {{ errors[0] }}
    div(v-if="!error")
      div(v-if="isBuy").mt-4.has-text-grey-light {{$t('exchange.applied_fee')}} {{ fee }} BTC {{$t('exchange.fee_in_simba')}}
      div(v-else).mt-4.has-text-grey-light {{$t('exchange.applied_fee')}} ≈ {{ (+fee * 100000000) }} SIMBA
    div(v-if="error").error.has-text-danger.mt-4 {{ $t('exchange.amount_err') }} 200,000 SIMBA
</template>

<script>
  import { ValidationProvider } from "vee-validate";
  //import {Money} from 'v-money'

  export default {
    name: 'trade-create-payment',

    components: {ValidationProvider},

    data: () => ({
      accepted_terms: false,
      isConverting: false,
      error: false,
      btc: 0.0025,
      simba: 200000,
      fee: 0,
      btn_loading: false,
      money: {
        thousands: ' ',
        precision: 0,
        masked: false
      },
      invoice_id: '',
      check_btc_address_interval: null
    }),

    created() {
      this.fee = 0.0005

      if(!this.isBuy) {
        this.btc = 0.0015
        this.simba = 200000
      }
    },

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

        if(this.simba < 200000) {
          this.error = true
          return
        }

        this.btn_loading = true;
        this.$store.commit('exchange/setTradeData', { prop: 'simba', value: this.simba })
        this.$store.commit('exchange/setTradeData', { prop: 'btc', value: this.btc })

        // create transaction
        let created_invoice = await this.$store.dispatch('invoices/createTransaction', this.tradeData.operation);

        this.$store.commit('exchange/setTradeData', {prop: 'invoice_id', value: created_invoice._id})

        if(this.isBuy) {
          this.check_btc_address_interval = setInterval(async () => {
            let invoice = await this.checkBitcoinAddress(created_invoice._id)

            if(invoice.target_btc_address) {
              clearInterval(this.check_btc_address_interval)
              this.btn_loading = false
              let data_for_update = {
                id: created_invoice._id,
                eth_address: this.tradeData.eth_address,
                simba_amount: this.tradeData.simba,
                btc_amount: this.tradeData.btc * 100000000
              }

              // Update invoice with amounts
              let updated_invoice_res = await this.$store.dispatch('invoices/updateTransaction', data_for_update)

              // Add invoice id to url, go to next step
              if(updated_invoice_res) {
                this.$nuxt.$router.push({ path: '/exchange/buysell', query: {id: invoice._id }})
                //this.$parent.$emit('nextStep')
              }
            }
          }, 3000)
        } else {
          let data_for_update = {
            id: created_invoice._id,
            btc_address: this.tradeData.btc_redeem_wallet,
            eth_address: this.tradeData.eth_address,
            simba_amount: this.tradeData.simba,
            btc_amount: this.tradeData.btc * 100000000
          }
          // Update invoice with amounts
          let updated_invoice_res = await this.$store.dispatch('invoices/updateTransaction', data_for_update)
          this.btn_loading = false

          // Add invoice id to url, go to next step
          if(updated_invoice_res) {
            this.$nuxt.$router.push({ path: '/exchange/buysell', query: {id: created_invoice._id }})
            //this.$parent.$emit('nextStep')
          }
        }
      },

      checkMinimum() {
        if(this.simba < 200000) {
          this.error = true
        } else {
          this.error = false
        }
      },

      convert() {
        if(this.isConverting) {
          return
        }

        let res_in_btc = +((this.simba/100000000).toFixed(8));

        if(isNaN(res_in_btc)) {
          this.btc = 0
        } else {
          if(res_in_btc > 0.0005) {
            if(this.isBuy) {
              this.btc = +parseFloat((res_in_btc + 0.0005).toFixed(8))
            } else {
              this.btc = +parseFloat((res_in_btc - 0.0005).toFixed(8))
            }
            this.fee = 0.0005
          } else {
            this.btc = 0
            this.fee = 0
          }
        }

        this.checkMinimum()
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
          let simba = (this.btc*100000000)
          let simba_with_fee = 0

          if(this.isBuy) {
            simba_with_fee = (simba - 50000).toFixed(0)
            this.fee = simba > 50000 ? 0.0005 : 0
          } else {
            if(this.btc > 0) {
              simba_with_fee = (simba + 50000).toFixed(0)
              this.fee = 0.0005
            } else {
              simba_with_fee = 0
              this.fee = 0
            }
          }

          this.simba = simba_with_fee < 1 ? 0 : simba_with_fee
        }

        this.isConverting = false
        this.checkMinimum()
      }
    }
  }
</script>

<style lang="sass" scoped>
  .checkbox-fix:not(.button)
    margin-right: 0
</style>
