<template lang="pug">
  div
    div.is-size-5.has-text-weight-bold {{$t('su_invoices.invoice')}} {{$t('exchange.cancelled_or_expired').toLocaleLowerCase()}}
    div.mt-4.is-flex.align-items-center
      div.column.is-4.p-0.is-size-6 {{$t('exchange.time_is_out')}}
      n-link(to="/exchange/").btn {{$t('other.try_again')}}
    div.is-flex.align-items-center.countdown-block.mt-4
      Countdown(:date="invoice.created_at").mr-4
      div.countdown-refresh.mr-4
        img(:src="require('~/assets/images/countdown-refresh.svg')")
      div {{$t('exchange.time_is_limited')}}
</template>

<script>
import {mapGetters, mapState} from 'vuex'
import Countdown from '~/components/Countdown'
import invoiceMixins from '~/mixins/invoiceMixins'

export default {
  name: 'trade-final',
  mixins: [invoiceMixins],
  components: {Countdown},
  data: () => ({}),
  computed: {
    ...mapGetters('exchange', ['isBuyInvoice']),
    ...mapState('exchange', ['invoice']),
  },
}
</script>

<style lang="sass"></style>
