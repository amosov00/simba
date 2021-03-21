<template lang="pug">
  div
    div(v-if="!expired")
      h3.text-large.has-text-weight-bold {{ $t('exchange.bill_payment')}}
      div.mt-2(v-if="isBuyInvoice")
        div.is-flex.align-items-center
          img(:src="require('~/assets/images/bitcoin-new.png')" style="height: 36px").mr-2
          div.text-large.is-flex.align-items-center {{ $t('exchange.send')}}
            = ' '
            span.has-text-weight-bold.ml-1 {{ btcFormat(invoice.btc_amount) }} BTC
            = ' '
            span.bill-arrow
              img(:src="require('~/assets/images/arrow-right.svg')")

          div.flex-1.is-flex.align-items-center
            template(v-if="invoice.target_btc_address")
              span.text-large {{ invoice.target_btc_address }}
              CopyToClipboard(:value_to_copy="invoice.target_btc_address").ml-2
              TradeQRCode(:qrcode_value="invoice.target_btc_address" :amount="btcFormat(invoice.btc_amount)").ml-1

        div.is-flex.align-items-center.mt-2
          img(:src="require('~/assets/images/logo_sm.png')").mr-2
          div.text-large.is-flex.align-items-center {{ $t('exchange.receive')}}
            = ' '
            span.has-text-weight-bold.ml-1 {{ simbaFormat(+invoice.simba_amount - 50000) }} SIMBA
            span.bill-arrow
              img(:src="require('~/assets/images/arrow-right.svg')")
            span {{ invoice.target_eth_address }}

      div.mt-2(v-else)
        div.is-flex.align-items-center
          img(:src="require('~/assets/images/logo_sm.png')").mr-2
          div.text-large.is-flex.align-items-center.w-100 {{ $t('exchange.send')}}
            = ' '
            span.has-text-weight-bold.ml-1 {{ simbaFormat(+invoice.simba_amount) }} SIMBA
            span.bill-arrow
              img(:src="require('~/assets/images/arrow-right.svg')")
            span {{ truncateHash(adminEthHash) }}
            CopyToClipboard(:value_to_copy="adminEthHash").ml-2
            TradeQRCode(:qrcode_value="adminEthHash" :amount="parseFloat(invoice.simba_amount)").ml-1
            button.btn(@click="payWithMetamask" style="margin-left: auto" :disabled="disablePayBtn") {{ $t('other.send') }}

        div.is-flex.align-items-center.mt-2
          img(:src="require('~/assets/images/bitcoin-new.png')" style="height: 36px").mr-2
          div.text-large.is-flex.align-items-center {{ $t('exchange.receive')}}
            = ' '
            span.has-text-weight-bold.ml-1 {{ btcFormat(invoice.btc_amount) }} BTC
            = ' '
            span.bill-arrow
              img(:src="require('~/assets/images/arrow-right.svg')")
            span {{ invoice.target_btc_address }}

    div.mt-4(v-if="expired")
      div.has-text-weight-bold.is-size-5 {{$t('exchange.bill_expired')}}
      div.mt-3.is-flex.align-items-center
        div.column.is-4.p-0.is-size-6 {{$t('exchange.time_is_out')}}
        n-link(to="/exchange/").btn {{$t('other.try_again')}}
    div.is-flex.align-items-center.countdown-block
      Countdown(:date="invoice.created_at" v-if="showCountdown" @expired="onExpired").mr-4
      div.countdown-refresh.mr-4(:class="{ 'rotate-anim': loading }" @click="manualInvoiceFetch")
        img(:src="require('~/assets/images/countdown-refresh.svg')")
      div(v-if="!expired")
        div {{$t('exchange.verify_auto')}}
        div {{$t('exchange.verify_asap')}}
      div(v-if="expired") {{$t('exchange.time_is_limited')}}

</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from 'vuex'

import Countdown from '~/components/Countdown'
import CopyToClipboard from '~/components/CopyToClipboard'
import TradeQRCode from '~/components/TradeQRCode'
import AddressQRCode from '~/components/AddressQRCode'

import invoiceMixins from '~/mixins/invoiceMixins'
import formatCurrency from '~/mixins/formatCurrency'

export default {
  name: 'trade-bill-payment',

  components: { Countdown, CopyToClipboard, TradeQRCode, AddressQRCode },
  mixins: [formatCurrency, invoiceMixins],

  props: {
    loading: Boolean,
    manualInvoiceFetch: Function,
  },

  computed: {
    ...mapGetters('exchange', ['isBuyInvoice']),
    ...mapState('exchange', ['invoice', 'operation', 'adminEthHash']),
  },
  data: () => ({
    expired: false,
    showCountdown: false,
    countdown: null,
    disablePayBtn: false,
  }),
  methods: {
    ...mapActions("exchange", ["fetchAdminEthAddress"]),
    onExpired() {
      this.expired = true
      // this.$parent.$emit('step_failed')
    },
    async payWithMetamask() {
      let data = {
        address: this.adminEthHash,
        amount: this.invoice.simba_amount,
      }

      if (await this.$store.dispatch('contract/transferSimbaToken', data)) {
        this.disablePayBtn = true
      }
    },
  },

  async created() {
    await this.fetchAdminEthAddress()
    this.showCountdown = true
  },
}
</script>

<style lang="sass" scoped>
@keyframes rotate
  to
    transform: rotate(360deg)
.rotate-anim
  opacity: 0.4
  animation: 1s rotate infinite linear
.countdown-block
  margin-top: 43px

.countdown-refresh
  cursor: pointer
  position: relative
  &.rotate-anim
    &:hover
      cursor: default
  &:hover
    opacity: 0.8
  &:active
    opacity: 0.6

.bill-arrow
  display: inline-block
  align-items: center
  vertical-align: center
  margin: 0 30px

.trade-timer
  margin-top: 50px
  font-style: normal
  font-weight: 100
  font-size: 36px
  line-height: 100%
  color: #000000
</style>
