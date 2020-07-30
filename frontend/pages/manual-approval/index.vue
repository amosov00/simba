<template lang="pug">
  div.main-content
    h1.title.is-size-4 Manual payout approval
    //--div.has-text-grey-light
      div.mb-3 {{ meta }}
      div {{ manualPayout }}
    div.is-flex.space-between.mt-4.mb-3.align-items-center
      div
        div.is-flex.align-items-center.is-size-6.mb-2
          span.mr-2 Status:
          div.mr-2.has-text-weight-bold {{ manualPayout ? 'Enabled' : 'Disabled'}}
        button.btn(@click="changeManualPayoutStatus") Change status
        div.is-flex.align-items-center.mt-4
          b-switch(v-model="onlyWithProcessingStatus" @input="showProcessingOnly")
          span.ml-1 With 'Processing' status only
      div
        button.btn--outlined(@click="$fetch") Refresh
    b-table(:loading="isLoading" :data="invoicesToView" hoverable paginated per-page="20" default-sort="created_at" default-sort-direction="desc").mt-2
      template(slot-scope="props")
        b-table-column(field="created_at" :label="$i18n.t('su_invoices.created_at')" sortable) {{ timestampFromUtc(props.row.created_at) }}
        b-table-column(field="tx_hashes" label="Transactions")
          div
            //--div.has-text-weight-bold ETH transcations:
            div(v-for="(hash, i) in props.row.eth_tx_hashes" :key="i" style="white-space: nowrap")
              span.has-text-weight-bold eth:
              =' '
              b-tooltip(:label="hash")
                a(:href="getBlockchainLink(hash, 'tx', 'eth')" target="blank" rel="noopener noreferrer") {{ truncateHash(hash) }}
          div.mt-2
            //-- div.has-text-weight-bold BTC transcations:
            div(v-for="(hash, i) in props.row.btc_tx_hashes" :key="i" style="white-space: nowrap")
              span.has-text-weight-bold btc:
              =' '
              b-tooltip(:label="hash")
                a(:href="getBlockchainLink(hash, 'tx', 'btc')" target="blank" rel="noopener noreferrer") {{ truncateHash(hash) }}
        b-table-column(field="btc_amount" label="BTC (Payout)" sortable) {{ btcFormat(props.row.btc_amount) }}
        b-table-column(field="simba_amount" label="SIMBA" sortable) {{ simbaFormat(props.row.simba_amount) }}
        b-table-column(field="actions" label="Actions")
          button.manual-btn(:disabled="props.row.status !== 'processing'" @click="makeDecision('pay', props.row._id)") pay
          button.manual-btn.manual-btn--red(:disabled="props.row.status !== 'processing'" @click="makeDecision('cancel', props.row._id)") cancel
        //--b-table-column(field="_id" label="ID" width="50" sortable)
          n-link(:to="`/invoices/${props.row._id}`") {{ truncateHash(props.row._id) }}
        //--b-table-column(field="user_id" :label="$i18n.t('su_invoices.user_id')" width="50" sortable)
          n-link(:to="`/users/${props.row.user_id}`") {{ truncateHash(props.row.user_id) }}
        b-table-column(field="target_btc_address" label="Target BTC")
          b-tooltip(:label="props.row.target_btc_address")
            a(:href="getBlockchainLink(props.row.target_btc_address, 'address', 'btc')" target="blank" rel="noopener noreferrer") {{ truncateHash(props.row.target_btc_address) }}
        b-table-column(field="status" :label="$i18n.t('su_invoices.status')" sortable) {{ props.row.status }}

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
      makeDecision(type, id) {
        this.$buefy.dialog.confirm({
          message: 'Please confirm your action',
          cancelText: this.$i18n.t('other.cancel'),
          confirmText: this.$i18n.t('other.confirm'),
          type: type === 'cancel' ? 'is-danger' : 'is-primary',
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

      truncateHash(hash) {

        if(!hash) {
          return ''
        } else if(typeof hash !== 'string') {
          return ''
        }

        return `${hash.substring(0, 6)}...${hash.substring(hash.length - 12)}`
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

<style lang="sass">
  .manual-btn
    border: 0
    background: #028a36
    color: #ffffff
    padding: 4px 8px
    border-radius: 3px
    display: block
    margin-bottom: 4px
    min-width: 65px
    text-align: center
    &:hover:not(:disabled)
      cursor: pointer
      opacity: 0.9
    &:last-child
      margin-right: 0
    &--red
      background: #FA172F
    &:disabled
      background: #acacac
</style>
