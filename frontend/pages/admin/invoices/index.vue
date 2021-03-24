<template lang="pug">
  div.main-content
    div.is-flex.is-justified-between.mb-3
      h1.is-size-4 {{$t('su_invoices.invoices')}}
      b-select(v-model="status").mr-3.wallet-select
        template(v-for="op in statusOptions")
          option(:value="op") {{ $i18n.t(`exchange.statuses.${op}`) }}
    div.mb-3
      b-input(v-model="searchQuery" @input="onSearchInput" :placeholder="`${this.$i18n.t('other.search')}...`" icon="magnify")
    div(v-if="adminInvoices.length <= 0") {{ $t('other.search_empty_results') }}
    b-table(v-if="adminInvoices.length > 0 && table" :data="adminInvoices" paginated per-page="20" default-sort="created_at" default-sort-direction="desc")
      template(slot-scope="props")
        b-table-column(field="created_at" :label="$i18n.t('su_invoices.created_at')" width="150" sortable) {{ timestampFromUtc(props.row.created_at) }}
        b-table-column(field="_id" label="ID" width="50" sortable)
          n-link(:to="`/admin/invoices/${props.row._id}`") {{ props.row._id }}
        b-table-column(field="user_id" :label="$i18n.t('su_invoices.user_id')" width="50" sortable)
          n-link(:to="`/admin/users/${props.row.user_id}`") {{ (props.row.user_id) }}
        b-table-column(field="status" :label="$i18n.t('su_invoices.invoice_type')"  width="100" sortable)
          span {{ $t(`su_invoices.invoice_type_${props.row.invoice_type}`) }}
        b-table-column(field="status" :label="$i18n.t('su_invoices.status')"  width="100" sortable)
          b-select(
            v-if="userStatus[props.row._id].status === 'suspended'"
            v-model="userStatus[props.row._id].status"
            @input="(s)=>changeStatus(s, props.row._id)"
            :loading="userStatus[props.row._id].loading"
          )
            template(v-for="op in editStatusOptions")
              option(:value="op") {{ $i18n.t(`exchange.statuses.${op}`) }}
          span(v-else :style="{color: InvoiceStatusToColor(props.row.status)}") {{ $t(`exchange.statuses.${props.row.status}`) }}
        b-table-column(field="btc_amount" label="BTC"  width="50" sortable) {{ btcFormat(props.row.btc_amount) }}
        b-table-column(field="simba_amount" label="SIMBA"  width="50" sortable) {{ simbaFormat(props.row.simba_amount) }}

</template>

<script>
import _ from 'lodash'
import {mapGetters, mapActions} from 'vuex';

import formatDate from '~/mixins/formatDate'
import formatCurrency from '~/mixins/formatCurrency'
import {InvoiceStatus, InvoiceStatusToColor} from '@/consts'

export default {
  name: 'invoices',
  layout: 'main',
  middleware: ['adminRequired'],
  mixins: [formatDate, formatCurrency],
  watch: {
    async status(value) {
      await this.fetchPaidInvoiced(value)
    },
  },
  async created() {
    if (this.adminInvoices.length <= 0) {
      await this.fetchAdminInvoices({q: this.searchQuery})
    }
    // TODO refactor this
    this.adminInvoices.forEach((item) => {
      this.$set(this.userStatus, item._id, {status: item.status, loading: false})
    })
    this.table = true
  },
  data: () => ({
    searchQuery: '',
    status: 'all',
    userStatus: {},
    table: false
  }),
  computed: {
    ...mapGetters("invoices", ["adminInvoices"]),
    statusOptions() {
      return [...Object.values(InvoiceStatus), 'all']
    },
    editStatusOptions() {
      return [InvoiceStatus.PROCESSING, InvoiceStatus.COMPLETED, InvoiceStatus.CANCELLED, InvoiceStatus.SUSPENDED]
    }
  },
  methods: {
    ...mapActions("invoices", ["fetchAdminInvoices", "changeInvoiceStatus"]),
    InvoiceStatusToColor,
    onSearchInput: _.debounce(async function () {
      let properSearchQuery = this.searchQuery.toLowerCase().trim()

      if (properSearchQuery !== '' || properSearchQuery.length <= 0) {
        await this.fetchAdminInvoices({q: properSearchQuery})
      }
    }, 500),
    async fetchPaidInvoiced(status) {
      const searchQuery = this.searchQuery.toLowerCase().trim()
      const payload = {}
      payload.q = searchQuery
      if (status !== null) {
        payload.status = status
      }
      await this.fetchAdminInvoices(payload)
    },
    async changeStatus(status, id) {
      try {
        this.userStatus[id].status = 'suspended'
        this.userStatus[id].loading = true
        await this.changeInvoiceStatus({id,status})
        this.userStatus[id].status = status
        this.$buefy.toast.open({message: 'Succesfully changed!', type: 'is-primary'})
      } catch (e) {
        console.log(e)
        this.$buefy.toast.open({message: 'Error changing status!', type: 'is-danger'})
      } finally {
        this.userStatus[id].loading = false
      }
    }
  },
}
</script>

<style lang="sass" scoped>
.is-justified-between
  justify-content: space-between
</style>
