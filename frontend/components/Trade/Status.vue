<template lang="pug">
  div.position-relative
    h3.text-large.has-text-weight-bold Status
    div.mt-3.is-size-6 Received payment {{ parseFloat(convert(received_payment_amount)) }} BTC
    div.mt-2 Transaction hash:
      =' '
      a(:href="'https://etherscan.io/tx/' + tx_hash" target="_blank").link {{ tx_hash }}
    div.mt-2
      div Confirmation 1/1
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

    props: {
      multi_props: Object,
    },

    async created() {
      let res = await this.$store.dispatch('invoices/fetchSingle', this.multi_props['invoice']);
      this.received_payment_amount = res.btc_amount_proceeded

      if(res.btc_txs.length > 0) {
        this.tx_hash = res.btc_txs[0].hash || ''
      }
    },

    mounted() {
      this.interval = setInterval(async () => {
        this.loadingSpinner()
        let res = await this.$store.dispatch('invoices/fetchSingle', this.multi_props['invoice'])

        if(res.status === 'completed') {

          if(!this.$parent.multi_props.hasOwnProperty("buy_info")) {
            this.$parent.multi_props["buy_info"] = {}
          }

          this.$parent.multi_props["buy_info"]["simba_issued"] = res.btc_amount_proceeded
          this.$parent.multi_props["buy_info"]["target_eth"] = res.target_eth_address
          this.$parent.multi_props["buy_info"]["tx_hash"] = res.btc_txs[0].hash

          this.$parent.multi_props["invoice"] = res._id

          clearInterval(this.interval)
          this.$parent.$emit('nextStep')
        }
        console.log('checking on Status comp')
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
