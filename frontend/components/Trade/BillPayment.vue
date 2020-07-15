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
            CopyToClipboard(:value_to_copy="btc_address").ml-2
            TradeQRCode(:qrcode_value="btc_address" :amount="parseFloat(tradeData.btc)").ml-1
        div.is-flex.align-items-center.mt-2
          img(src="@/assets/images/logo_sm.png").mr-2
          div.text-large.is-flex.align-items-center {{ $t('exchange.receive')}}
            = ' '
            span.has-text-weight-bold.ml-1 {{ simbaFormat(tradeData.simba) }} SIMBA
            span.bill-arrow
              img(:src="require('@/assets/images/arrow-right.svg')")
            span {{ updated_invoice_data.target_eth_address }}
      div.mt-2(v-else)
        div.is-flex.align-items-center
          img(src="@/assets/images/logo_sm.png").mr-2
          div.text-large.is-flex.align-items-center.w-100 {{ $t('exchange.send')}}
            = ' '
            span.has-text-weight-bold.ml-1 {{ tradeData.simba }} SIMBA
            span.bill-arrow
              img(:src="require('@/assets/images/arrow-right.svg')")
            span {{ truncateEthAddress(tradeData.admin_eth_address) }}
            CopyToClipboard(:value_to_copy="tradeData.admin_eth_address").ml-2
            TradeQRCode(:qrcode_value="tradeData.admin_eth_address" :amount="parseFloat(tradeData.simba)").ml-1
            button.btn(@click="payWithMetamask" style="margin-left: auto") {{ $t('other.send') }}
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
      div.has-text-weight-bold.is-size-5 {{$t('exchange.bill_expired')}}
      div.mt-3.is-flex.align-items-center
        div.column.is-4.p-0.is-size-6 {{$t('exchange.time_is_out')}}
        n-link(to="/exchange/").btn {{$t('other.try_again')}}
    div.is-flex.align-items-center.countdown-block
      Countdown(:date="updated_invoice_data.created_at" v-if="showCountdown").mr-4
      div.countdown-refresh.mr-4(:class="{ 'rotate-anim': busyChecking }" @click="checkSingle")
        img(:src="require('@/assets/images/countdown-refresh.svg')")
      div(v-if="!expired")
        div {{$t('exchange.verify_auto')}}
        div {{$t('exchange.verify_asap')}}
      div(v-if="expired") {{$t('exchange.time_is_limited')}}

</template>

<script>
  import Countdown from "~/components/Countdown";
  import formatCurrency from '~/mixins/formatCurrency'

  import CopyToClipboard from "~/components/CopyToClipboard";
  import TradeQRCode from "~/components/TradeQRCode";

  import AddressQRCode from "~/components/AddressQRCode";

  export default {
    name: 'trade-bill-payment',

    components: {Countdown, CopyToClipboard, TradeQRCode, AddressQRCode},
    mixins: [formatCurrency],

    computed: {
      isBuy(){
        return this.$store.getters['exchange/tradeData']['operation'] === 1;
      },
      btc_address() {
        return this.updated_invoice_data.target_btc_address;
      },
      tradeData() {
        return this.$store.getters['exchange/tradeData'];
      },
      created_invoice_id() {
        return this.$store.getters['exchange/tradeData']['invoice_id']
      }
    },
    data: () => ({
      expired: false,
      busyChecking: false,
      transaction_hash: '',
      updated_invoice_data: {
      },
      check: {},
      showCountdown: false,
      countdown: null,
      goneToNextStep: false,
      confirmInterval: null,
    }),
    methods: {
      truncateEthAddress(address) {
        return `${address.substring(0, 6)}...${address.substring(address.length - 4)}`
      },

      payWithMetamask() {
        let transferData = {
          address: this.tradeData.admin_eth_address,
          amount: this.tradeData.simba
        }

        let transfer = this.$store.dispatch("contract/transferSimbaToken", transferData);
      },

      stopCountdown() {
        if(this.countdown !== null) {
          clearInterval(this.countdown)
        }
      },

      async checkSingle() {
        this.busyChecking = true

        this.check = await this.$store.dispatch('invoices/fetchSingle', this.created_invoice_id)

        if(this.isBuy) { // Buy
          if(this.check.btc_txs.length > 0) {
            this.goneToNextStep = true
            this.stopCountdown();
            this.$parent.$emit('nextStep')
            return;
          }
        } else { // Sell
          if(this.check.eth_txs.length > 0) {
            if(this.check.eth_txs[0].bitcoins_sended) {
              this.goneToNextStep = true
              this.stopCountdown();
              this.$parent.$emit('nextStep')
              return;
            }
          }
        }

        this.updated_invoice_data = JSON.parse(JSON.stringify(this.check));

        // Confirm if invoice is not confirmed
        if(this.updated_invoice_data.target_btc_address && this.updated_invoice_data.status === 'created') {
          await this.$store.dispatch('invoices/confirmTransaction', this.created_invoice_id)
        }

        await setTimeout(() => {
          this.busyChecking = false;
        }, 1000)
      }
    },

    async created() {
      this.$on('expired', () => {
        this.expired = true
        this.stopCountdown()
        this.$parent.$emit('step_failed')
      })

      await this.$store.dispatch('exchange/fetchAdminEthAddress')

      await this.checkSingle()

      this.$store.commit('exchange/setTradeData', { prop: 'simba', value: this.updated_invoice_data.simba_amount })
      this.$store.commit('exchange/setTradeData', { prop: 'btc', value: (this.updated_invoice_data.btc_amount/100000000).toFixed(8) })

      this.showCountdown = true;

      if(!this.goneToNextStep) {
        this.countdown = setInterval(async () => {
          await this.checkSingle();
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
