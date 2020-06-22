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
      div.mt-2 Created transaction: {{ created_transaction }}
      div.mt-2 Checking your transaction every 10 sec...
      div.mt-2 Status: {{ status }}
      div.mt-4(v-if="Object.keys(updated_invoice_data).length !== 0") Recived info:
        span(v-if="updated_invoice_data.btc_txs.length === 0") empty
      div.mt-1(v-if="Object.keys(updated_invoice_data).length !== 0")
        div(v-for="(item, i) in updated_invoice_data.btc_txs" :key="i").mt-4 {{ i+1 }}
          |) {{ item._id }}
          div.mt-2 simba_tokens_issued: {{ item.simba_tokens_issued }}
          div.mt-2 confirmations: {{ item.confirmations }}
          div.mt-2 total: {{ item.total }}
      b-loading(:active.sync="busyChecking" :is-full-page="false")
    div.mt-4
      Countdown(:date="updated_invoice_data.created_at" v-if="showCountdown")
    div.mt-4
      b-input(placeholder="transaction hash" v-model="transaction_hash")
      b-button.btn.mt-2(@click="setTransaction") Set transaction hash
</template>

<script>
  import Countdown from "~/components/Countdown";

  export default {
    name: 'trade-bill-payment',

    components: {Countdown},

    props: {
      multi_props: Object
    },

    computed: {
      btc_address() {
        return this.$store.getters.btc_address;
      },
      tradeData() {
        return this.$store.getters['exchange/tradeData'];
      }
    },
    data: () => ({
      busyChecking: false,
      status: '',
      transaction_hash: '',
      created_transaction: '',
      updated_invoice_data: {
      },
      check: {},
      showCountdown: false
    }),
    methods: {
      async setTransaction() {

        let res = await this.$store.dispatch('invoices/manualTransaction', { id: this.created_transaction, transaction_hash: this.transaction_hash });
        console.log(res);
      },

      async checkSingle() {
        this.busyChecking = true
        this.check = await this.$store.dispatch('invoices/fetchSingle', this.created_transaction)
        this.status = this.check.status
        this.updated_invoice_data = JSON.parse(JSON.stringify(this.check));
        this.busyChecking = false;
      }
    },

    async created() {
      if(this.multi_props['no_create']) {
        console.log('multi-props', this.multi_props);
        this.created_transaction = this.multi_props['invoice'];

      } else {

        let tradeData = this.$store.getters['exchange/tradeData'];
        let res = await this.$store.dispatch('invoices/createTransaction', tradeData.operation);

        this.created_transaction = res._id

        let eth_address = this.$store.getters['exchange/tradeData']['eth_address'];
        let updateData = { id: this.created_transaction, eth_address, simba_amount: tradeData.simba}
        let res2 = await this.$store.dispatch('invoices/updateTransaction', updateData)

        console.log('update transaction: ', res2)

        let res3 = await this.$store.dispatch('invoices/confirmTransaction', this.created_transaction)

        console.log('confirm transaction: ', res3)
      }


      // Preload BTC address
      await this.$store.dispatch('getBtcAddress')

      await this.checkSingle()

      this.showCountdown = true;

      setInterval(async () => {
        this.busyChecking = true;
        await this.checkSingle();
        await setTimeout(() => {
          this.busyChecking = false
        }, 1000)
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
