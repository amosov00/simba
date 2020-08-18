<template lang="pug">
  div
    div.position-relative
      h3.text-large.has-text-weight-bold {{$t('exchange.status')}}
      div.mt-3.is-size-6 {{$t('exchange.received_payment')}} {{ simbaFormat(received_payment_amount) }} SIMBA
      div.mt-2 {{$t('exchange.transaction_hash')}}:
        =' '
        a(:href="'https://etherscan.io/tx/' + tx_hash" target="_blank").link {{ tx_hash }}
      div.mt-2
        div {{$t('exchange.confirms')}} {{currentConfirms}}/{{min_confirms}}
      b-loading(:active.sync="confirms_loading" :is-full-page="false")
</template>

<script>
  import formatCurrency from '~/mixins/formatCurrency'

  import invoiceMixins from "~/mixins/invoiceMixins";

  export default {
    name: 'trade-btc-sent',
    data: () => ({
      interval: null,
      confirms_loading: false,
      tx_hash: '',
      received_payment_amount: 0,
      min_confirms: 3,
      currentConfirms: 0
    }),
    mixins: [formatCurrency, invoiceMixins],

    computed: {
      isProd() {
        return process.env.NODE_ENV === 'production'
      },

      tradeData() {
        return this.$store.getters['exchange/tradeData']
      },
    },

    async created() {
      // this.min_confirms = process.env.NODE_ENV === 'develop' || 'development' ? 1 : 3

      let res = await this.$store.dispatch('invoices/fetchSingle', this.tradeData.invoice_id);
      this.received_payment_amount = res.simba_amount_proceeded

      let transfer_confirms = this.findEthTransactionByEvent(res, 'Transfer')?.confirmations;

      this.currentConfirms = transfer_confirms > this.min_confirms ? this.min_confirms : transfer_confirms

      if(res.eth_txs.length > 0) {
        this.tx_hash = this.findEthTransactionByEvent(res, 'Transfer')?.transactionHash || ''
      }
    },

    beforeDestroy() {
      clearInterval(this.interval)
      this.interval = null
    },

    mounted() {
      this.interval = setInterval(async () => {
        this.loadingSpinner()
        let res = await this.$store.dispatch('invoices/fetchSingle', this.tradeData.invoice_id)

        let desired_tx = this.findEthTransactionByEvent(res, 'Transfer')

        this.currentConfirms = desired_tx?.confirmations > this.min_confirms ? this.min_confirms : desired_tx?.confirmations

        if(res.eth_txs.length > 0) {
          if(res.eth_txs[0].confirmations >= this.min_confirms && res.btc_txs.length > 0) {
            this.$store.commit('exchange/setTradeData', { prop: 'simba_issued', value: res.btc_amount_proceeded})
            this.$store.commit('exchange/setTradeData', { prop: 'tx_hash', value: res.btc_txs[0].hash })

            clearInterval(this.interval)
            this.$parent.$emit('nextStep')
          }
        }
      }, 10000)
    },

    methods: {
      loadingSpinner() {
        this.confirms_loading = true
        setTimeout(() => {
          this.confirms_loading = false
        }, 1000)
      },

      convert(simba) {

        let test = (simba/100000000).toFixed(8);

        if(isNaN(test)) {
          return 0
        }

        return test
      },
    }
  }
</script>

<style lang="sass">
</style>
