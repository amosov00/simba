<template lang="pug">
  div
    div.main-content(style="padding-left: 10px; padding-right: 10px")
      h1.title.is-size-4 {{ $t('su_payouts_mm.manage_payouts.full') }}
      div.is-flex.space-between.mt-4.mb-3.align-items-center
        div
          div.is-flex.align-items-center.is-size-6.mb-2
            span.mr-2 {{ $t('su_payouts_mm.status') }}:
            div.mr-2.has-text-weight-bold {{ manualPayout ? $t('su_payouts_mm.enabled') : $t('su_payouts_mm.disabled')}}
          button.btn(@click="changeManualPayoutStatus") {{ $t('su_payouts_mm.change_status') }}
      div.is-flex.align-items-center(style="justify-content: center")
        div.is-flex.align-items-center.mr-4
          b-switch(v-model="onlyWithProcessingStatus" @input="showProcessingOnly")
          span.ml-1 {{ $t('su_payouts_mm.processing_only') }}
        button.btn--outlined(@click="$fetch" :disabled="isLoading") {{ $t('su_payouts_mm.refresh') }}
      b-table(:loading="isLoading" :data="invoicesToView" hoverable paginated per-page="20" default-sort="created_at" default-sort-direction="desc").mt-4
        template(slot-scope="props")
          b-table-column(field="created_at" :label="$i18n.t('su_payouts_mm.date')" width="140" sortable)
            span.is-size-7 {{ timestampFromUtc(props.row.created_at) }}
          b-table-column(field="_id" label="ID" sortable)
            n-link(:to="`/invoices/${props.row._id}`") {{ truncateHash(props.row._id, 4, 6) }}
          b-table-column(field="tx_hashes" :label="$i18n.t('su_payouts_mm.transactions')" width="200")
            div
              div(v-for="(hash, i) in props.row.eth_tx_hashes" :key="i" style="white-space: nowrap")
                span.has-text-weight-bold eth:
                =' '
                b-tooltip(:label="hash")
                  a(:href="getBlockchainLink(hash, 'tx', 'eth')" target="blank" rel="noopener noreferrer") {{ truncateHash(hash) }}
            div.mt-2
              div(v-for="(hash, i) in props.row.btc_tx_hashes" :key="i" style="white-space: nowrap")
                span.has-text-weight-bold btc:
                =' '
                b-tooltip(:label="hash")
                  a(:href="getBlockchainLink(hash, 'tx', 'btc')" target="blank" rel="noopener noreferrer") {{ truncateHash(hash) }}
          b-table-column(field="btc_amount" label="BTC" sortable) {{ btcFormat(props.row.btc_amount) }}
          b-table-column(field="simba_amount" label="SIMBA" sortable width="100") {{ simbaFormat(props.row.simba_amount) }}
          b-table-column(field="actions" :label="$i18n.t('su_payouts_mm.actions')" width="180")
            button.manual-btn(:disabled="props.row.status !== 'processing' || props.row.btc_tx_hashes.length > 0" @click="makeDecision('pay', props.row._id, props.row.target_btc_address, btcFormat(props.row.btc_amount))") {{ $t('su_payouts_mm.pay') }}
            button.manual-btn.manual-btn--red(:disabled="props.row.status !== 'processing'" @click="makeDecision('cancel', props.row._id, props.row.target_btc_address, btcFormat(props.row.btc_amount))") {{ $t('su_payouts_mm.cancel') }}
          b-table-column(field="target_btc_address" :label="$i18n.t('su_payouts_mm.target_address')" width="120")
            b-tooltip(:label="props.row.target_btc_address")
              a(:href="getBlockchainLink(props.row.target_btc_address, 'address', 'btc')" target="blank" rel="noopener noreferrer") {{ truncateHash(props.row.target_btc_address) }}
          b-table-column(field="status" :label="$i18n.t('su_invoices.status')" sortable) {{ $t(`exchange.statuses.${props.row.status}`) }}

</template>

<script>
  import formatDate from "~/mixins/formatDate";
  import formatCurrency from "~/mixins/formatCurrency";

  import moment from 'moment'
  import _ from 'lodash'

  import invoiceMixins from "~/mixins/invoiceMixins";

  export default {
    layout: "main",
    middleware: ["adminRequired"],
    mixins: [formatDate, formatCurrency, invoiceMixins],

    data: () => ({
      onlyWithProcessingStatus: false,
      invoices: [],
      invoicesToView: [],
      isLoading: false,
    }),

    async fetch() {
      this.isLoading = true

      this.invoices = await this.$store.dispatch('invoices/fetchAdminInvoices')

      this.invoicesToView = this.invoices.filter(inv => inv.invoice_type === 2)

      if(this.onlyWithProcessingStatus) {
        this.invoicesToView = this.invoicesToView.filter(inv => inv.status === 'processing')
      }

      this.isLoading = false
    },

    computed: {
      meta() {
        return this.$store.getters['meta/meta']
      },
      manualPayout() {
        return this.$store.getters['meta/meta'].find(el => {
          return el.slug === 'manual_payout'
        })?.payload?.is_active
      }
    },

    methods: {
      makeDecision(type, id, targetWallet, amount) {

        let message = `<div>ID: <strong>${id}</strong></div>` +
          `<div class="mt-1">Target address: <strong>${targetWallet}</strong></div>` +
          `<div class="mt-1">Amount: <strong>${amount}</strong></div>`;

        if(type === 'cancel') {
          message = `<div class="mb-3">${this.$i18n.t('su_payouts_mm.confirm_cancel_msg')}</div>` + message

        } else if (type === 'pay') {
          message = `<div class="mb-3">${this.$i18n.t('su_payouts_mm.confirm_pay_msg')}</div>` + message
        }

        this.$buefy.dialog.confirm({
          title: this.$i18n.t('xpub.confirm_your_action'),
          message,
          cancelText: this.$i18n.t('other.cancel'),
          confirmText: this.$i18n.t('other.confirm'),
          type: type === 'cancel' ? 'is-danger' : 'is-success',
          onConfirm: async () => {
            this.isLoading = true

            if(await this.$store.dispatch('meta/invoiceDecision', { type, id })) {
              this.$buefy.toast.open({message: 'Success', type:'is-primary'})
              this.$fetch()
            } else {
              this.$buefy.toast.open({message: 'Something went wrong', type:'is-danger'})
            }


            this.isLoading = false
          }
        })

      },

      showProcessingOnly() {
        if(this.onlyWithProcessingStatus) {
          this.invoicesToView = this.invoices.filter(inv => inv.status === 'processing')
        } else {
          this.invoicesToView = this.invoicesToView = this.invoices
        }
      },

      truncateHash(hash, fromStart = 6, fromEnd = 12) {

        if(!hash) {
          return ''
        } else if(typeof hash !== 'string') {
          return ''
        }

        return `${hash.substring(0, fromStart)}...${hash.substring(hash.length - fromEnd)}`
      },

      changeManualPayoutStatus() {
        this.$buefy.dialog.confirm({
          title: this.$i18n.t('xpub.confirm_your_action'),
          message: this.$i18n.t('xpub.confirm_change_status'),
          cancelText: this.$i18n.t('other.cancel'),
          confirmText: this.$i18n.t('other.confirm'),
          type: this.manualPayout ? 'is-danger' : 'is-primary',
          onConfirm: async () => {
            let data = {
              is_active: !this.manualPayout
            }

            if(await this.$store.dispatch('meta/updateMeta', { data, slug: 'manual_payout'})) {
              await this.$store.dispatch('meta/fetchMeta')
              this.$buefy.toast.open({message: 'Status successfully changed!', type: 'is-primary'})
            } else {
              this.$buefy.toast.open({message: 'Error changing status', type: 'is-danger'})
            }
          }

        })
      }
    },

    async asyncData({store}) {
      await store.dispatch('meta/fetchMeta')
    }
  };
</script>

<style lang="sass" scoped>
  .manual-btn
    border: 0
    background: #0ACA62
    color: #ffffff
    padding-top: 4px
    padding-bottom: 4px
    border-radius: 3px
    margin-right: 4px
    margin-bottom: 4px
    width: 70px
    text-align: center
    font-size: 12px
    &:hover:not(:disabled)
      cursor: pointer
      opacity: 0.9
    &:last-child
      margin-right: 0
    &--red
      background: #DC6161
    &:disabled
      background: #c1c1c1
</style>
