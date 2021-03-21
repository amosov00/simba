<template lang="pug">
  div
    div.main-content
      div.position-relative
        n-link(to="/exchange/")
          img(src="~assets/images/back.svg").back-btn
      div.steps.is-flex.align-items-center
        div.operation.mr-4(v-if="operation") {{ $t(`exchange.${operation.toLowerCase()}`) }}
        span(v-for="i in generateSteps()" :key="i" :class="{ 'steps-item--failed': isFailStep(i), 'steps-item--active': isActiveStep(i)}").steps-item {{ i+1 }}
      div.trade-content
        component(:is="currentStepComponent" :loading="loading" :manualInvoiceFetch="proceedInvoice")
</template>

<script>
import _ from 'lodash';
import {mapActions, mapMutations, mapState} from 'vuex'

import {
  BillPayment,
  Cancelled,
  ChooseWallet,
  Completed,
  ConfirmInvoice,
  WatchingIncomingTransactions,
  WatchingOutcomingTransactions,
  Suspended
} from "~/components/Trade";
import {InvoiceStatus, InvoiceTypeEnum, InvoiceTypeToText} from "~/consts";

export default {
  name: 'exchange-buysell',
  layout: 'main',
  components: {
    ChooseWallet, // step 1
    ConfirmInvoice, // step 2
    BillPayment, // step 3
    WatchingIncomingTransactions, // step 4
    WatchingOutcomingTransactions, // step 5
    Completed, // step 6
    Cancelled, // step 6
    Suspended, // step 6
  },

  data: () => {
    return {
      InvoiceStatus,
      InvoiceTypeEnum,
      interval: null,
      stepFail: null,
      loading: false,
      stepsAmount: 6,
      tradeData: {
        ethAddress: '',
        steps: {
          current: 'ChooseWallet',
          list: ['ChooseWallet', 'ConfirmInvoice', 'BillPayment', 'Status', 'Final'],
        },
      },
    }
  },

  computed: {
    ...mapState("exchange", ["invoiceId", "invoice", "operation", "currentStepComponent", "currentStepIndicatorIndex", "fetchInvoiceDataLoop"]),
  },

  methods: {
    ...mapActions("invoices", ["fetchSingleInvoice"]),
    ...mapMutations(["setMetamaskEthAddress"]),
    ...mapMutations("exchange", [
      "setTradeData",
      "setInvoice",
      "setInvoiceId",
      "setCurrentStepComponent",
      "setCurrentStepIndicatorIndex",
      "clearState",
      "setFetchInvoiceDataLoop",
      "setOperation",
    ]),
    typeToText: InvoiceTypeToText,
    generateSteps() {
      return _.range(this.stepsAmount)
    },
    nextStep() {
      let {steps} = this.tradeData
      this.tradeData.steps.current = steps.list[steps.list.indexOf(steps.current) + 1]
    },

    isFailStep(i) {

      return [this.InvoiceStatus.CANCELLED, this.InvoiceStatus.SUSPENDED].includes(this.invoice?.status) && i === this.stepsAmount - 1
    },
    isActiveStep(i) {
      return this.isFailStep(i) ? false : i <= this.currentStepIndicatorIndex
    },
    async proceedInvoice() {
      if (!this.invoiceId) {
        return
      }
      this.loading = true
      let invoice = await this.fetchSingleInvoice(this.invoiceId)

      if (invoice) {
        this.setInvoice(invoice)
        this.setOperation(this.typeToText(invoice.invoice_type))
        switch (invoice.status) {
          case InvoiceStatus.CREATED:
            this.setCurrentStepComponent("ConfirmInvoice")
            this.setCurrentStepIndicatorIndex(1)
            this.setFetchInvoiceDataLoop(false)
            break;
          case InvoiceStatus.WAITING:
            this.setCurrentStepComponent("BillPayment")
            this.setCurrentStepIndicatorIndex(2)
            this.setFetchInvoiceDataLoop(true)
            break;
          case InvoiceStatus.PROCESSING:
            this.setCurrentStepIndicatorIndex(3)
            this.setCurrentStepComponent("WatchingIncomingTransactions")
            this.setFetchInvoiceDataLoop(true)
            break
          case InvoiceStatus.PAID:
            this.setCurrentStepIndicatorIndex(4)
            this.setCurrentStepComponent("WatchingOutcomingTransactions")
            this.setFetchInvoiceDataLoop(true)
            break;
          case InvoiceStatus.CANCELLED:
            this.setCurrentStepComponent("Cancelled")
            this.setCurrentStepIndicatorIndex(5)
            this.setFetchInvoiceDataLoop(false)
            break;
          case InvoiceStatus.SUSPENDED:
            this.setCurrentStepComponent("Suspended")
            this.setCurrentStepIndicatorIndex(5)
            this.setFetchInvoiceDataLoop(false)
            break;
          case InvoiceStatus.COMPLETED:
            this.setCurrentStepComponent("Completed")
            this.setCurrentStepIndicatorIndex(5)
            this.setFetchInvoiceDataLoop(false)
            break;
          default:
            break
        }
      }

      this.loading = false
    },
  },

  async mounted() {
    if (this.$nuxt.$route.query.op) {
      this.setOperation(this.$nuxt.$route.query['op'])
    }
    if (this.$nuxt.$route.query.id) {
      this.setInvoiceId(this.$nuxt.$route.query['id'])
    }
    await this.proceedInvoice()

    this.interval = setInterval(async () => {
      if (this.fetchInvoiceDataLoop) {
        await this.proceedInvoice()
      }
    }, 10000)
  },


  async beforeDestroy() {
    clearInterval(this.interval)
    this.interval = null
    this.clearState()
  },


  async hello() {
    // if (this.$nuxt.$route.query['op']) {
    //   if (this.$nuxt.$route.query['op'] === 'buy') {
    //     this.operation = 'Buy'
    //     this.$store.commit('exchange/setTradeData', { prop: 'operation', value: 1 })
    //   } else {
    //     this.operation = 'Sell'
    //     this.$store.commit('exchange/setTradeData', { prop: 'operation', value: 2 })
    //     this.tradeData.steps.list.splice(3, 0, 'SimbaRecieved')
    //   }
    // }

    // Handle url with invoice id
    if (this.$nuxt.$route.query['id']) {
      let single_res = await this.$store.dispatch('invoices/fetchSingleInvoice', this.$nuxt.$route.query['id'])

      this.$store.commit('exchange/setTradeData', {
        prop: 'invoice_id',
        value: this.$nuxt.$route.query['id'],
      })

      if (single_res) {
        if (single_res.invoice_type === 1) {
          this.operation = 'Buy'
          this.$store.commit('exchange/setTradeData', {prop: 'operation', value: 1})
        } else {
          this.operation = 'Sell'
          this.$store.commit('exchange/setTradeData', {prop: 'operation', value: 2})
          this.tradeData.steps.list.splice(3, 0, 'SimbaRecieved')
        }

        if (single_res.status === 'waiting' || single_res.status === 'created') {
          this.$store.commit('exchange/setTradeData', {prop: 'btc', value: single_res.btc_amount})
          this.$store.commit('exchange/setTradeData', {prop: 'simba', value: single_res.simba_amount})
          this.tradeData.steps.current = 'BillPayment'
        } else if (single_res.status === 'processing') {
          if (single_res.btc_txs.length > 0 && single_res.eth_txs.length > 0) {
            this.tradeData.steps.current = 'Status'
          } else if (single_res.eth_txs.length > 0) {
            this.tradeData.steps.current = 'SimbaRecieved'
          }
        } else if (single_res.status === 'paid' || single_res.status === 'completed') {
          this.$store.commit('exchange/setTradeData', {prop: 'eth_txs', value: single_res.eth_txs})
          this.$store.commit('exchange/setTradeData', {prop: 'btc_txs', value: single_res.btc_txs})
          if (single_res.invoice_type === 1) {
            this.$store.commit('exchange/setTradeData', {
              prop: 'btc_amount_proceeded',
              value: single_res.btc_amount_proceeded,
            })
            this.$store.commit('exchange/setTradeData', {prop: 'target_eth', value: single_res.target_eth_address})
            this.$store.commit('exchange/setTradeData', {prop: 'tx_hash', value: single_res.eth_tx_hashes[0] || ''})
            this.$store.commit('exchange/setTradeData', {
              prop: 'simba_issued',
              value: single_res.btc_amount_proceeded,
            })
          } else {
            this.$store.commit('exchange/setTradeData', {
              prop: 'simba_issued',
              value: single_res.btc_amount_proceeded,
            })
            this.$store.commit('exchange/setTradeData', {
              prop: 'btc_redeem_wallet',
              value: single_res.target_btc_address,
            })
            this.$store.commit('exchange/setTradeData', {prop: 'tx_hash', value: single_res.btc_txs[0].hash})
            this.$store.commit('exchange/setTradeData', {
              prop: 'tx_hash_redeem',
              value: single_res.eth_txs[0]?.transactionHash || single_res.eth_tx_hashes[0],
            })
          }
          this.tradeData.steps.current = 'Final'
        } else if (single_res.status === 'cancelled') {
          this.tradeData.steps.current = 'BillPayment'
          /*this.$buefy.toast.open({message:'Invoice cancelled!', type: 'is-danger'})
            this.$nuxt.context.redirect('/exchange/')*/
        }
      } else {
        this.$buefy.toast.open({message: 'Error: invoice not found', type: 'is-danger'})
        this.$nuxt.context.redirect('/exchange/')
      }
    }
  },
}
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
