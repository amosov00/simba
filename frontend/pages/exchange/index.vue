<template lang="pug">
  div
    div.main-content
      div
        n-link(to="/exchange/buysell?op=buy").btn.mr-2 Buy
        n-link(to="/exchange/buysell?op=sell").btn.mr-2 Sell
      h3.title.is-5.mt-4 Last bills
      div.bills-table
        n-link(:to="'/exchange/buysell?id=' + item._id" v-for="(item, i) in billsToShow" :key="i").is-flex.bills-table__container
          div {{ item._id }}
          div {{ item.simba_amount }}
          div {{ (new Date(item.created_at)).toLocaleString() }}
          div {{ getType(item.invoice_type) }}
          div {{ item.status }}
      div.has-text-centered
        button.mt-3.btn--outlined(@click="showMore" v-if="showBtn") More
</template>

<script>
  export default {
    name: "exchange-index",
    layout: 'main',
    computed: {
      invoiceData() {
        let array_data = JSON.parse(JSON.stringify(this.$store.getters['invoices/invoices'])).reverse();

        let amount = this.amounToView;

        return array_data.slice(0, amount);
      }
    },
    data: () => ({
      amounToView: 4,
      billsToShow: [],
      showBtn: true
    }),

    mounted() {
      //this.showMore()
      this.billsToShow = this.billsList.slice(0, this.amounToView)
    },

    methods: {
      showMore() {
        this.amounToView += 10

        if(this.amounToView >= this.billsList.length) {
          this.showBtn = false
          this.amounToView = this.billsList.length
        }

        this.billsToShow = this.billsList.slice(0, this.amounToView)
      },

      getType(type) {
        if(type ===  2){ return 'SELL'}

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
