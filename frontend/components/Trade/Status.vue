<template lang="pug">
  div.position-relative
    h3.text-large.has-text-weight-bold Status
    div.mt-3.is-size-6 Received payment {{ parseFloat(convert(received_payment_amount)) }} BTC
    div.mt-2 Transaction hash:
      =' '
      a(:href="'https://etherscan.io/tx/' + tx_hash" target="_blank").link {{ tx_hash }}
    div.mt-2
      div Confirmation 1/{{min_confirms}}
    b-loading(:active.sync="confirms_loading" :is-full-page="false")
</template>

<script>
  export default {
    name: 'trade-status',
    data: () => ({
      interval: null,
      confirms_loading: false,
      tx_hash: '',
      received_payment_amount: 0,
      min_confirms: 1
    }),

    computed: {
      tradeData() {
        return this.$store.getters['exchange/tradeData']
      }
    },

    async created() {
      let res = await this.$store.dispatch('invoices/fetchSingle', this.tradeData.invoice_id);
      this.received_payment_amount = res.btc_amount_proceeded

      if(res.btc_txs.length > 0) {
        this.tx_hash = res.eth_txs[0]?.hash || ''
      }
    },

    mounted() {
      this.interval = setInterval(async () => {
        this.loadingSpinner()
        let res = await this.$store.dispatch('invoices/fetchSingle', this.tradeData.invoice_id)

        if(res.status === 'completed' || res.btc_txs[0].confirmations >= this.min_confirms) {

          this.$store.commit('exchange/setTradeData', { prop: 'simba_issued', value: res.btc_amount_proceeded})
          this.$store.commit('exchange/setTradeData', { prop: 'target_eth', value: res.target_eth_address})
          this.$store.commit('exchange/setTradeData', { prop: 'tx_hash', value: res.eth_txs[0]?.hash || ''})

          clearInterval(this.interval)
          this.$parent.$emit('nextStep')
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
