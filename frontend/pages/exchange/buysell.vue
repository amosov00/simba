<template lang="pug">
  div
    div.main-content
      div.position-relative
        n-link(to="/exchange/")
          img(src="~assets/images/back.svg").back-btn
      div.steps.is-flex.align-items-center
        div.operation.mr-4 {{ $t(`exchange.${operation.toLowerCase()}`) }}
        span(v-for="(step, i) in tradeData.steps.list" :key="i" :class="{ 'steps-item--failed': failedStep(i), 'steps-item--active': activeStep(i)}").steps-item {{ i+1 }}
      div.trade-content
        component(:is="tradeData.steps.current")
</template>

<script>
  import WalletConfirm from "@/components/Trade/WalletConfirm"
  import CreatePayment from "@/components/Trade/CreatePayment"
  import BillPayment from "@/components/Trade/BillPayment"
  import Status from "@/components/Trade/Status"
  import SimbaRecieved from "~/components/Trade/SimbaRecieved"
  import Final from "@/components/Trade/Final"

  import { ToastProgrammatic as Toast } from 'buefy'

  export default {
    name: "exchange-buysell",
    layout: 'main',
    components: { WalletConfirm, CreatePayment, BillPayment, Status, Final, SimbaRecieved },

    methods: {
      activeStep(i) {
        if(this.failedStep(i)) {
          return false
        }

        return i < (this.tradeData.steps.list.indexOf(this.tradeData.steps.current)+1)
      },

      failedStep(i){
        if(this.stepFail) {
          if(i === this.stepFail) {
            return true
          }
        }

        return false
      }
    },

    async middleware ({ redirect, store }) {
      if (window.ethereum !== undefined) {
        await window.ethereum.enable().then(res => {
          store.commit('exchange/setTradeData', { prop: 'eth_address', value: res[0]})
          return true
        }).catch(_ => {
          redirect('/exchange/')
          return false
        })
      } else {

        Toast.open({message: 'Metamask is not installed!', type:'is-danger', duration: 4000})

        redirect('/exchange/')
      }
    },

    beforeRouteUpdate (to, from, next) {
      if(to.query.hasOwnProperty('id')) {
        this.tradeData.steps.current = 'BillPayment'
      }
      next()
    },

    async beforeMount() {
      this.$on('nextStep', () => {
        let steps = this.tradeData.steps;
        steps.current = steps.list[steps.list.indexOf(steps.current)+1]
      });

      this.$on('step_failed', () => {
        this.stepFail = this.tradeData.steps.list.indexOf(this.tradeData.steps.current)
      })


      if(this.$nuxt.$route.query['op']) {
        if(this.$nuxt.$route.query['op'] === 'buy') {
          this.operation = 'Buy';
          this.$store.commit('exchange/setTradeData', {prop: 'operation', value: 1})
        } else {
          this.operation = 'Sell'
          this.$store.commit('exchange/setTradeData', {prop: 'operation', value: 2})
          this.tradeData.steps.list.splice(3, 0, 'SimbaRecieved')
        }
      }

      // Handle url with invoice id
      if(this.$nuxt.$route.query['id']) {
        let single_res = await this.$store.dispatch('invoices/fetchSingle', this.$nuxt.$route.query['id']);

        this.$store.commit('exchange/setTradeData', {
          prop: 'invoice_id', value: this.$nuxt.$route.query['id']
        })

        if(single_res) {

          if(single_res.invoice_type === 1) {
            this.operation = 'Buy';
            this.$store.commit('exchange/setTradeData', {prop: 'operation', value: 1})
          } else {
            this.operation = 'Sell'
            this.$store.commit('exchange/setTradeData', {prop: 'operation', value: 2})
            this.tradeData.steps.list.splice(3, 0, 'SimbaRecieved')
          }

          if(single_res.status === 'waiting' || single_res.status === 'created') {
            this.$store.commit('exchange/setTradeData', {prop: 'btc', value: single_res.btc_amount})
            this.$store.commit('exchange/setTradeData', {prop: 'simba', value: single_res.simba_amount})
            this.tradeData.steps.current = 'BillPayment'
          }
          else if(single_res.status === 'processing') {
            if(single_res.btc_txs.length > 0 && single_res.eth_txs.length > 0) {
              this.tradeData.steps.current = 'Status'
            } else if (single_res.eth_txs.length > 0){
              this.tradeData.steps.current = 'SimbaRecieved'
            }
          }
          else if(single_res.status === 'completed') {
            if(single_res.invoice_type === 1) {
              this.$store.commit('exchange/setTradeData', {prop: 'btc_amount_proceeded', value: single_res.btc_amount_proceeded})
              this.$store.commit('exchange/setTradeData', {prop: 'target_eth', value: single_res.target_eth_address})
              this.$store.commit('exchange/setTradeData', {prop: 'tx_hash', value: single_res.eth_tx_hashes[0] || ''})
              this.$store.commit('exchange/setTradeData', {prop: 'simba_issued', value: single_res.btc_amount_proceeded})
            } else {
              this.$store.commit('exchange/setTradeData', {prop: 'simba_issued', value: single_res.btc_amount_proceeded})
              this.$store.commit('exchange/setTradeData', { prop: 'btc_redeem_wallet', value: single_res.target_btc_address})
              this.$store.commit('exchange/setTradeData', { prop: 'tx_hash', value: single_res.btc_txs[0].hash })
              this.$store.commit('exchange/setTradeData', { prop: 'tx_hash_redeem', value: single_res.eth_txs[0]?.transactionHash || single_res.eth_tx_hashes[0] })
              this.$store.commit('exchange/setTradeData', { prop: 'eth_txs', value: single_res.eth_txs })
            }

            this.tradeData.steps.current = 'Final'
          }
          else if(single_res.status === 'cancelled') {
            this.tradeData.steps.current = 'BillPayment'
            /*this.$buefy.toast.open({message:'Invoice cancelled!', type: 'is-danger'})
            this.$nuxt.context.redirect('/exchange/')*/
          }
        } else {
          this.$buefy.toast.open({message:'Error: invoice not found', type: 'is-danger'})
          this.$nuxt.context.redirect('/exchange/')
        }

      }
    },

    data: () => {
      return {
        stepFail: null,
        operation: '',
        tradeData: {
          ethAddress: '',
          steps: {
            current: 'WalletConfirm',
            list: ['WalletConfirm', 'CreatePayment', 'BillPayment', 'Status', 'Final']
          }
        },
      }
    }
  };
</script>

<style lang="sass" scoped>
  .trade-content
    margin-top: 50px

  .operation
    font-weight: bold
    font-size: 22px
    line-height: 144.19%
    color: #E0B72E
</style>
