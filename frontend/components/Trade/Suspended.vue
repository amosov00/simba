<template lang="pug">
  div
    div.has-text-danger.is-size-5.has-text-weight-bold {{$t('exchange.suspended_title')}}
    div.mt-2
      div {{btcFormat(limits.btc_used, 2)}} BTC / {{btcFormat(limits.btc_limit, 2)}} BTC
    div.mt-2.is-size-5
      span.has-text-weight-bold {{ amount }}
      =' '
      span {{$t('exchange.suspended_help_text')}}
    div.mt-2 {{$t('exchange.wallet')}}:
      =' '
      a(:href="walletLink" target="_blank").link {{ walletAddress }}

    div.mt-4
      //b-button.btn.mr-4(href='#' disabled) {{$t('exchange.contact_support')}}
      b-button.btn(tag="router-link" to='/profile/verification/' :disabled="kyc.is_verified") {{$t('exchange.upgradeTier2')}}
</template>

<script>
import _ from 'lodash'
import { mapActions, mapGetters, mapState } from 'vuex'
import invoiceMixins from '~/mixins/invoiceMixins'
import formatCurrency from '~/mixins/formatCurrency'

export default {
  name: 'trade-suspended',
  mixins: [invoiceMixins, formatCurrency],
  data: () => ({}),
  computed: {
    ...mapGetters(["kyc"]),
    ...mapGetters('exchange', ['isBuyInvoice']),
    ...mapState('exchange', ['invoice', 'operation', 'limits', 'currencyRate']),
    amount() {
      if (this.isBuyInvoice) {
        return `${this.simbaFormat(this.invoice.btc_amount_proceeded)} SIMBA`
      } else {
        return `${this.btcFormat(this.invoice.simba_amount_proceeded)} BTC`
      }
    },
    walletAddress() {
      return this.isBuyInvoice ? this.invoice.target_eth_address : this.invoice.target_btc_address
    },
    walletLink() {
      return this.getBlockchainLink(this.walletAddress, 'address', this.isBuyInvoice ? 'eth' : 'btc')
    },
  },
  methods: {
    ...mapActions('exchange', ['fetchLimits', 'fetchCurrencyRate']),
    ...mapActions(["getKYCStatus"])
  },
  async mounted() {
    await this.fetchLimits()

    if (_.isEmpty(this.kyc)) {
      await this.getKYCStatus()
    }
  },
}
</script>

<style lang="sass"></style>
