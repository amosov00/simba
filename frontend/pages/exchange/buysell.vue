<template lang="pug">
  div
    div.main-content
      div.position-relative
        n-link(to="/exchange/")
          img(:src="require('~/assets/images/back.svg')").back-btn
      div.steps.is-flex.align-items-center
        div.operation.mr-4(v-if="operation") {{ $t(`exchange.${operation.toLowerCase()}`) }}
        span(v-for="i in generateSteps()" :key="i" :class="{ 'steps-item--failed': isFailStep(i), 'steps-item--active': isActiveStep(i)}").steps-item {{ i+1 }}
      div.trade-content
        component(:is="currentStepComponent" :loading="loading" :manualInvoiceFetch="proceedInvoice")
</template>

<script>
import _ from 'lodash'
import { mapActions, mapMutations, mapState } from 'vuex'

import {
  Waiting,
  Cancelled,
  ChooseWallet,
  Completed,
  ConfirmInvoice,
  WatchingIncomingTransactions,
  WatchingOutcomingTransactions,
  Suspended,
} from '~/components/Trade'
import { InvoiceStatus, InvoiceTypeEnum, InvoiceTypeToText } from '~/consts'

export default {
  name: 'exchange-buysell',
  layout: 'main',
  components: {
    ChooseWallet, // step 1
    ConfirmInvoice, // step 2
    Waiting, // step 3
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
    }
  },

  computed: {
    ...mapState('exchange', [
      'invoiceId',
      'invoice',
      'operation',
      'currentStepComponent',
      'currentStepIndicatorIndex',
      'fetchInvoiceDataLoop',
    ]),
  },

  methods: {
    ...mapActions('invoices', ['fetchSingleInvoice']),
    ...mapMutations(['setMetamaskEthAddress']),
    ...mapMutations('exchange', [
      'setInvoice',
      'setInvoiceId',
      'setCurrentStepComponent',
      'setCurrentStepIndicatorIndex',
      'clearState',
      'setFetchInvoiceDataLoop',
      'setOperation',
    ]),
    InvoiceTypeToText,
    generateSteps() {
      return _.range(this.stepsAmount)
    },
    isFailStep(i) {
      return (
        [this.InvoiceStatus.CANCELLED, this.InvoiceStatus.SUSPENDED].includes(this.invoice?.status) &&
        i === this.stepsAmount - 1
      )
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
        this.setOperation(this.InvoiceTypeToText(invoice.invoice_type))
        switch (invoice.status) {
          case InvoiceStatus.CREATED:
            this.setCurrentStepComponent('ConfirmInvoice')
            this.setCurrentStepIndicatorIndex(1)
            this.setFetchInvoiceDataLoop(false)
            break
          case InvoiceStatus.WAITING:
            this.setCurrentStepComponent('Waiting')
            this.setCurrentStepIndicatorIndex(2)
            this.setFetchInvoiceDataLoop(true)
            break
          case InvoiceStatus.PROCESSING:
            this.setCurrentStepIndicatorIndex(3)
            this.setCurrentStepComponent('WatchingIncomingTransactions')
            this.setFetchInvoiceDataLoop(true)
            break
          case InvoiceStatus.PAID:
            this.setCurrentStepIndicatorIndex(4)
            this.setCurrentStepComponent('WatchingOutcomingTransactions')
            this.setFetchInvoiceDataLoop(true)
            break
          case InvoiceStatus.CANCELLED:
            this.setCurrentStepComponent('Cancelled')
            this.setCurrentStepIndicatorIndex(5)
            this.setFetchInvoiceDataLoop(false)
            break
          case InvoiceStatus.SUSPENDED:
            this.setCurrentStepComponent('Suspended')
            this.setCurrentStepIndicatorIndex(5)
            this.setFetchInvoiceDataLoop(false)
            break
          case InvoiceStatus.COMPLETED:
            this.setCurrentStepComponent('Completed')
            this.setCurrentStepIndicatorIndex(5)
            this.setFetchInvoiceDataLoop(false)
            break
          default:
            break
        }
      } else {
        this.$buefy.toast.open({ message: 'Error: invoice not found', type: 'is-danger' })
        await this.$nuxt.context.redirect('/exchange/')
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
