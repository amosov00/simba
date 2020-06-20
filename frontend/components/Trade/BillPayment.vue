<template lang="pug">
  div
    h3.text-large.has-text-weight-bold Bill payment
    div.mt-2
      div.is-flex.align-items-center
        img(src="@/assets/images/bitcoin.svg").mr-2
        div.text-large Send
          = ' '
          span.has-text-weight-bold {{ tradeData.btc }} BTC
          = ' '
          | to {{ btc_address }}
      div.is-flex.align-items-center.mt-2
        img(src="@/assets/images/logo_sm.png").mr-2
        div.text-large To accept
          = ' '
          span.has-text-weight-bold {{ tradeData.simba }} SIMBA
    //- div.trade-timer 1:59:59
    div.position-relative
      div.mt-2 Created transaction: {{ new_transaction }}
      div.mt-2 Checking your transaction every 10 sec...
      div.mt-2 Status: {{ status }}
      b-loading(:active.sync="busyChecking" :is-full-page="false")
    div.mt-4
      n-link(to="/exchange").has-text-weight-bold Check bills
    div.mt-4
      b-input(placeholder="transaction hash" v-model="transaction_hash")
      b-button.btn.mt-2(@click="setTransaction") Set transaction hash

</template>

<script>
  export default {
    name: 'trade-bill-payment',
    computed: {
      btc_address() {
        return this.$store.getters.btc_address;
      },
      tradeData() {
        return this.$store.getters.tradeData;
      }
    },
    data: () => ({
      busyChecking: false,
      status: '',
      transaction_status: 0,
      transaction_status_list: ['not payed', 'payed!'],
      transaction_hash: '',
      new_transaction: ''
    }),
    methods: {
      async setTransaction() {

        let res = await this.$store.dispatch('invoices/manualTransaction', { id: new_transaction._id, transaction_hash: this.transaction_hash });
        console.log(res);
      }
    },
    async mounted() {
      await this.$store.dispatch('getBtcAddress')

      let res = await this.$store.dispatch('invoices/createTransaction', 1);

      this.new_transaction = res._id

      let tradeData = this.$store.getters['tradeData'];
      let metamask_address = this.$store.getters['metamask/address'];

      let updateData = { id: this.new_transaction, eth_address: metamask_address, simba_amount: tradeData.simba_amount}
      let res2 = await this.$store.dispatch('invoices/updateTransaction', updateData)

      console.log('update transaction: ', res2)

      let check;

      setInterval(async () => {
        this.busyChecking = true
        check = await this.$store.dispatch('invoices/fetchSingle', this.new_transaction)

        this.status = check.status
        await setTimeout(() => {
          this.busyChecking = false
        }, 1500)
      }, 10000)
    }
  }
</script>

<style lang="sass" scoped>
  .trade-timer
    margin-top: 50px
    font-style: normal
    font-weight: 100
    font-size: 36px
    line-height: 100%
    color: #000000
</style>
