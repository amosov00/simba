<template lang="pug">
  div
    div.is-size-5.has-text-weight-bold {{$t('su_invoices.invoice')}} {{$t('exchange.statuses.cancelled').toLocaleLowerCase()}}
    div.mt-4
      a(href="/exchange/buysell?op=buy" v-if="isBuyInvoice").btn {{$t('exchange.buy_more')}}
      a(href="/exchange/buysell?op=sell" v-else).btn {{$t('exchange.sell_more')}}
</template>

<script>
import {mapGetters, mapState} from 'vuex'
import invoiceMixins from '~/mixins/invoiceMixins'

export default {
  name: 'trade-final',
  mixins: [invoiceMixins],
  data: () => ({}),
  computed: {
    ...mapGetters('exchange', ['isBuyInvoice']),
  },
}
</script>

<style lang="sass"></style>
