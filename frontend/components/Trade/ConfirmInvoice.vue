<template lang="pug">
  div.mr-10
    h3.text-large.has-text-weight-bold {{$t('exchange.cr_payment_bill')}}
    div.is-flex.mt-2.align-items-center.space-between
      div.is-flex.align-items-center(:class="{ 'flex-row-reverse': isBuyInvoice}")
        div.is-flex.flex-column.align-items-center.smb-input-wrapper
          input(v-model="usdt" type="text" :disabled="true").smb-input
        span.mr-2.ml-2
          | {{$t('exchange.or')}}
        div.is-flex.flex-column.align-items-center.smb-input-wrapper
          input(v-model="simba" type="text" @input="convert" :disabled="loading").smb-input
        span.mr-2.ml-2
          | =
        div.is-flex.flex-column.align-items-center.smb-input-wrapper
          input(v-model="btc" type="text" @input="convertBTCtoSimba($event)" maxlength="10" :disabled="loading").smb-input

      n-link.btn(v-if="beyondLimit" to="/profile/verification/") {{$t('exchange.upgradeTier2')}}
      b-button.btn(v-else @click="confirm" :loading="loading" :disabled="!termsAccepted || error") {{$t('exchange.create')}}
    div.is-flex.space-between
      div.is-flex.has-text-centered(:class="{ 'flex-row-reverse': isBuyInvoice, 'justify-content-end': isBuyInvoice}")
        div.smb-input-wrapper.mt-2 USDT
        span.mr-4
        div.smb-input-wrapper.mt-2 SIMBA
        span.mr-4
        div.smb-input-wrapper.mt-2 BTC
      div
        ValidationProvider(:rules="{ required: { allowFalse: false } }" v-slot="{ errors }" :name="$i18n.t('auth.terms_of_agreement')" tag="div").mt-2
          b-checkbox(v-model="termsAccepted" :disabled="loading").checkbox-fix
            span {{$t('auth.i_accept')}}
            =' '
            a(href="https://simba.storage/terms-of-use.pdf" target="_blank" rel="noreferrer noopener").link {{$i18n.t('auth.terms_of_agreement')}}
          span.validaton-error {{ errors[0] }}
    div.mt-4 {{btcUsed}} BTC / {{btcLimit}} BTC
    div(v-if="!error")
      div(v-if="isBuyInvoice").mt-2.has-text-grey-light {{$t('exchange.applied_fee')}} {{ fee }} BTC {{$t('exchange.fee_in_simba')}}
      div(v-else).mt-2.has-text-grey-light {{$t('exchange.applied_fee')}} = {{ (+fee * 100000000) }} SIMBA
    div(v-if="error").error.has-text-danger.mt-2 {{ $t('exchange.amount_err') }} 200,000 SIMBA
    div(v-if="beyondLimit").error.has-text-danger.mt-2
      | {{$t('exchange["Above your limit"]')}} {{btcLimit}} BTC. {{$t('exchange.Please')}},
      n-link(to="/profile/verification/")  {{$t('exchange.update')}}
      |  {{$t('exchange["your verification level"]')}}.
</template>

<script>
import { mapActions, mapGetters, mapMutations, mapState } from 'vuex'

import { ValidationProvider } from 'vee-validate'
import { InvoiceTypeSlug, InvoiceTypeTextToEnum } from '~/consts'
//import {Money} from 'v-money'

export default {
  name: 'trade-confirm-invoice',

  components: { ValidationProvider },

  data: () => ({
    InvoiceTypeSlug,
    termsAccepted: false,
    isConverting: false,
    error: false,
    btc: 0.0025,
    usdt: 0,
    simba: 200000,
    fee: 0.00055,
    loading: false,
  }),

  async mounted() {
    if (this.operation === this.InvoiceTypeSlug.BUY) {
      this.btc = 0.0025
      this.simba = 200000
    } else {
      this.btc = 0.0015
      this.simba = 200000
    }
  },

  async created() {
    await this.fetchLimits()
    await this.fetchCurrencyRate()

    this.usdt = (this.btc * this.currencyRate.BTCUSD).toFixed(2)
  },

  computed: {
    ...mapGetters('exchange', ['isBuyInvoice']),
    ...mapState('exchange', ['invoice', 'invoiceId', 'operation', 'limits', 'currencyRate']),
    ...mapState(['metamaskEthAddress']),

    beyondLimit() {
      const { btc_limit, btc_used } = this.limits
      return this.btc * 10 ** 8 + btc_used > btc_limit
    },

    btcUsed() {
      return this.limits.btc_used ? (this.limits.btc_used / 10 ** 8).toFixed(6) : 0
    },
    btcLimit() {
      return this.limits.btc_limit ? this.limits.btc_limit / 10 ** 8 : 0
    },
  },

  watch: {
    btc() {
      this.usdt = (this.btc * this.currencyRate.BTCUSD).toFixed(2)
    },
  },

  methods: {
    ...mapMutations('exchange', ['setInvoiceId', 'setNextStep']),
    ...mapActions('exchange', ['fetchLimits', 'fetchCurrencyRate']),
    ...mapActions('invoices', ['createInvoice', 'updateInvoice', 'confirmInvoice']),

    async confirm() {
      if (this.simba < 200000) {
        this.error = true
        return
      }
      if (this.beyondLimit === true) {
        return
      }

      this.loading = true

      let updatedInvoice = await this.updateInvoice(
        this.isBuyInvoice
          ? {
              id: this.invoiceId,
              simba_amount: (this.btc * 10 ** 8).toFixed(0),
              btc_amount: (this.btc * 10 ** 8).toFixed(0),
            }
          : {
              id: this.invoiceId,
              simba_amount: this.simba.toFixed(0),
              btc_amount: (this.btc * 10 ** 8).toFixed(0),
            }
      )

      if (!updatedInvoice) {
        this.loading = false
        return
      }

      let invoiceConfirmed = await this.confirmInvoice(this.invoiceId)

      if (!invoiceConfirmed) {
        this.loading = false
        return
      }

      this.loading = false

      await this.setNextStep('Waiting')
    },

    checkMinimum() {
      this.error = this.simba < 200000
    },

    convert() {
      if (this.isConverting) {
        return
      }

      let res_in_btc = +(this.simba / 100000000).toFixed(8)

      if (isNaN(res_in_btc)) {
        this.btc = 0
      } else {
        if (res_in_btc > 0.0005) {
          if (this.isBuyInvoice) {
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
      let test = e.target.value

      if (isNaN(test)) {
        this.btc = 0
        this.simba = 0
      } else {
        this.btc = test
        let simba = this.btc * 100000000
        let simba_with_fee = 0

        if (this.isBuyInvoice) {
          simba_with_fee = (simba - 50000).toFixed(0)
          this.fee = simba > 50000 ? 0.0005 : 0
        } else {
          if (this.btc > 0) {
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
    },
  },
}
</script>

<style lang="sass" scoped>
.checkbox-fix:not(.button)
  margin-right: 0
</style>
