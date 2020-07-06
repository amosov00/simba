<template lang="pug">
  div
    div(v-if="!expired")
      h3.text-large.has-text-weight-bold {{ $t('exchange.bill_payment')}}
      div.mt-2(v-if="isBuy")
        div.is-flex.align-items-center
          img(src="@/assets/images/bitcoin.svg").mr-2
          div.text-large.is-flex.align-items-center {{ $t('exchange.send')}}
            = ' '
            span.has-text-weight-bold.ml-1 {{ parseFloat(tradeData.btc) }} BTC
            = ' '
            span.bill-arrow
              img(:src="require('@/assets/images/arrow-right.svg')")
            span {{ btc_address }}
        div.is-flex.align-items-center.mt-2
          img(src="@/assets/images/logo_sm.png").mr-2
          div.text-large.is-flex.align-items-center {{ $t('exchange.receive')}}
            = ' '
            span.has-text-weight-bold.ml-1 {{ tradeData.simba }} SIMBA
            span.bill-arrow
              img(:src="require('@/assets/images/arrow-right.svg')")
            span {{ updated_invoice_data.target_eth_address }}
      div.mt-2(v-else)
        div.is-flex.align-items-center
          img(src="@/assets/images/logo_sm.png").mr-2
          div.text-large.is-flex.align-items-center {{ $t('exchange.send')}}
            = ' '
            span.has-text-weight-bold.ml-1 {{ tradeData.simba }} SIMBA
            span.bill-arrow
              img(:src="require('@/assets/images/arrow-right.svg')")
            span {{ updated_invoice_data.target_eth_address }}
        div.is-flex.align-items-center.mt-2
          img(src="@/assets/images/bitcoin.svg").mr-2
          div.text-large.is-flex.align-items-center {{ $t('exchange.receive')}}
            = ' '
            span.has-text-weight-bold.ml-1 {{ parseFloat(tradeData.btc) }} BTC
            = ' '
            span.bill-arrow
              img(:src="require('@/assets/images/arrow-right.svg')")
            span {{ btc_address }}
    div.mt-4(v-if="expired")
      div.has-text-weight-bold.is-size-5 Bill expired
      div.mt-3.is-flex.align-items-center
        div.column.is-4.p-0.is-size-6 Time is out
        n-link(to="/exchange/").btn Try again
    div.is-flex.align-items-center.countdown-block
      Countdown(:date="updated_invoice_data.created_at" v-if="showCountdown").mr-4
      div.countdown-refresh.mr-4(:class="{ 'rotate-anim': busyChecking }" @click="checkSingle")
        img(:src="require('@/assets/images/countdown-refresh.svg')")
      div(v-if="!expired")
        div {{$t('exchange.verify_auto')}}
        div {{$t('exchange.verify_asap')}}
      div(v-if="expired") Time for each bill is limited with 2 hours.

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
      isBuy(){
        return this.multi_props.op === 'buy';
      },
      btc_address() {
/*        if(!this.isBuy) {
          return this.updated_invoice_data.target_btc_address;
        }

        return this.$store.getters.btc_address;*/

        return this.updated_invoice_data.target_btc_address;
      },
      tradeData() {
        return this.$store.getters['exchange/tradeData'];
      }
    },
    data: () => ({
      expired: false,
      busyChecking: false,
      status: '',
      transaction_hash: '',
      created_transaction: '',
      updated_invoice_data: {
      },
      check: {},
      showCountdown: false,
      countdown: null,
      goneToNextStep: false
    }),
    methods: {
      stopCountdown() {
        if(this.countdown !== null) {
          clearInterval(this.countdown)
        }
      },

      async setTransaction() {

        let res = await this.$store.dispatch('invoices/manualTransaction', { id: this.created_transaction, transaction_hash: this.transaction_hash });
        console.log(res);
      },

      async checkSingle() {
        if(!this.busyChecking) {
          this.busyChecking = true
          this.check = await this.$store.dispatch('invoices/fetchSingle', this.created_transaction)
          this.status = this.check.status

          if(this.check.btc_txs.length > 0) {
            if(this.check.btc_txs[0].confirmations > 0 ) {
              this.$parent.multi_props["invoice"] = this.check._id
              this.goneToNextStep = true
              this.stopCountdown();
              this.$parent.$emit('nextStep')
              return;
            }
          }

          this.updated_invoice_data = JSON.parse(JSON.stringify(this.check));
          await setTimeout(() => {
            this.busyChecking = false;
          }, 1000)
        }
      }
    },

    async created() {
      this.$on('expired', () => {
        this.expired = true
        this.stopCountdown()
        this.$parent.$emit('step_failed')
      })

      // Preload 'Hot' BTC address
      //await this.$store.dispatch('getBtcAddress')

      if(this.multi_props['no_create']) {
        this.created_transaction = this.multi_props['invoice'];
      } else {


        let tradeData = this.$store.getters['exchange/tradeData'];

        let res = await this.$store.dispatch('invoices/createTransaction', tradeData.operation);

        this.created_transaction = res._id

        let eth_address = this.$store.getters['exchange/tradeData']['eth_address'];
        //let btc_address = this.$store.getters['btc_address'];
        let btc_address = res.target_btc_address

        if(this.multi_props.op === 'sell') {
          btc_address = this.$store.getters['exchange/tradeData']['btc_target_wallet']
        }

        let updateData = { id: this.created_transaction, eth_address, btc_address, simba_amount: tradeData.simba}
        let res2 = await this.$store.dispatch('invoices/updateTransaction', updateData)

        console.log('id', this.created_transaction)

        let res3 = await this.$store.dispatch('invoices/confirmTransaction', this.created_transaction)

        console.log(res3);

        this.$nuxt.$router.push({ path: '/exchange/buysell', query: {id: this.created_transaction }})
      }

      await this.checkSingle()

      this.$store.commit('exchange/setTradeData', { prop: 'simba', value: this.updated_invoice_data.simba_amount })
      this.$store.commit('exchange/setTradeData', { prop: 'btc', value: (this.updated_invoice_data.btc_amount/100000000).toFixed(8) })

      this.showCountdown = true;

      if(!this.goneToNextStep) {
        this.countdown = setInterval(async () => {
          await this.checkSingle();
          console.log('Checking every 10 seconds!')
        }, 10000)
      }
    },

    beforeDestroy() {
      this.stopCountdown()
    }
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
