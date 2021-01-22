<template lang="pug">
  div
    div.main-content.is-flex.flex-column
      div
        n-link(to="/exchange/buysell?op=buy").btn.mr-2 {{ $t('exchange.buy') }}
        n-link(to="/exchange/buysell?op=sell").btn.mr-2 {{ $t('exchange.sell') }}
      h3.title.is-5.mt-4 {{ $t('exchange.last_bills') }}
      div.bills-table.flex-1(:class="{'is-flex': billsToShow.length === 0}")
        div(v-if="billsToShow.length === 0").no-bills {{ $t('exchange.empty_bills') }}
        n-link(:to="'/exchange/buysell?id=' + item._id" v-for="(item, i) in billsToShow" :key="i").is-flex.bills-table__container
          div {{ item._id }}
          div {{ simbaFormat(item.simba_amount) }}
          div {{ (new Date(item.created_at)).toLocaleString() }}
          div {{ getType(item.invoice_type) }}
          div(v-if="!getStatus(item).includes(':')") {{ $t(`exchange.statuses.${getStatus(item)}`) }}
          div(v-else) {{ getStatus(item) }}
      div.has-text-centered
        button.mt-3.btn--outlined(@click="showMore" v-if="showBtn") {{ $t('exchange.more_bills') }}
</template>

<script>
import moment from 'moment';

import formatCurrency from "~/mixins/formatCurrency";

export default {
  name: "exchange-index",
  layout: 'main',
  mixins: [formatCurrency],
  middleware: ["authRequired", "contract"],
  computed: {
    invoiceData() {
      let array_data = JSON.parse(JSON.stringify(this.$store.getters['invoices/invoices'])).reverse();

      let amount = this.amounToView;

      return array_data.slice(0, amount);
    }
  },
  data: () => ({
    amounToView: 6,
    billsToShow: [],
    showBtn: true
  }),

  mounted() {
    //this.showMore()
    this.billsToShow = this.billsList.slice(0, this.amounToView)
    if (!this.billsToShow.length) {
      this.showBtn = false
    }

    if (this.billsList.length <= this.amounToView) {
      this.showBtn = false
    }
  },

  methods: {
    getStatus(item) {
      if (item.status === 'waiting' || item.status === 'processing' || item.status === 'created') {
        let current = +Date.now();
        let dt = +moment.utc(item.created_at).toDate();

        let plus2hours = +dt + (2 * 60 * 60 * 1000)


        let diff = plus2hours - current;

        if (diff < 0) {
          //return 'expired'
          return '00:00:00'
        }

        let remain = moment.duration(diff);

        const twoDigits = (n) => {
          if (n < 10) {
            return `0${n}`
          }

          return n
        }

        return `${remain.hours()}:${twoDigits(remain.minutes())}:${twoDigits(remain.seconds())}`
      } else if (item.status === 'cancelled') {
        return 'expired'
      }

      return item.status
    },

    showMore() {
      this.amounToView += 10

      if (this.amounToView >= this.billsList.length) {
        this.showBtn = false
        this.amounToView = this.billsList.length
      }

      this.billsToShow = this.billsList.slice(0, this.amounToView)
    },

    getType(type) {
      if (type === 2) {
        return 'SELL'
      }

      return 'BUY'
    }
  },

  async asyncData({store}) {
    await store.dispatch('invoices/fetchInvoices');
    return {
      billsList: JSON.parse(JSON.stringify(store.getters['invoices/invoices'])).reverse()
    }
  }
};
</script>

<style lang="sass" scoped>
.no-bills
  display: flex
  align-items: center
  justify-content: center
  text-align: center
  color: #bcbcbc
  width: 100%

.bills-table
  border: 1px solid #EBEBEC

  &__container
    padding: 11px 0
    font-weight: 300
    font-size: 14px
    line-height: 100%
    color: #000000

    &:nth-child(even)
      background-color: #FAFAFA

    &:hover
      background-color: #EBEBEC

    div
      text-align: center

      &:first-child
        text-align: left
        padding-left: 40px

      &:last-child
        text-align: right
        padding-right: 40px

      &:nth-child(1)
        width: 20%

      &:nth-child(2)
        width: 30%

      &:nth-child(3)
        width: 20%

      &:nth-child(4)
        width: 20%

      &:nth-child(5)
        width: 20%
</style>
