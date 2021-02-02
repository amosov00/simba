<template lang="pug">
  div.main-content
    div.is-flex.is-justified-between.mb-3
      h1.is-size-4 {{$t('su_invoices.invoices')}}
      button.btn(@click="fetchPaidInvoiced") {{ $t('su_invoices.not_completed') }}
    div.mb-3
      b-input(v-model="searchQuery" @input="onSearchInput" :placeholder="`${this.$i18n.t('other.search')}...`" icon="magnify")
    div(v-if="adminInvoices.length <= 0") {{ $t('other.search_empty_results') }}
    b-table(v-if="adminInvoices.length > 0" :data="adminInvoices" paginated per-page="20" default-sort="created_at" default-sort-direction="desc")
      template(slot-scope="props")
        b-table-column(field="created_at" :label="$i18n.t('su_invoices.created_at')" width="150" sortable) {{ timestampFromUtc(props.row.created_at) }}
        b-table-column(field="_id" label="ID" width="50" sortable)
          n-link(:to="`/admin/invoices/${props.row._id}`") {{ props.row._id }}
        b-table-column(field="user_id" :label="$i18n.t('su_invoices.user_id')" width="50" sortable)
          n-link(:to="`/admin/users/${props.row.user_id}`") {{ (props.row.user_id) }}
        b-table-column(field="status" :label="$i18n.t('su_invoices.invoice_type')"  width="100" sortable)
          span {{ $t(`su_invoices.invoice_type_${props.row.invoice_type}`) }}
        b-table-column(field="status" :label="$i18n.t('su_invoices.status')"  width="100" sortable)
          span(:style="{color: statusToColor(props.row.status)}") {{ $t(`exchange.statuses.${props.row.status}`) }}
        b-table-column(field="btc_amount" label="BTC"  width="50" sortable) {{ btcFormat(props.row.btc_amount) }}
        b-table-column(field="simba_amount" label="SIMBA"  width="50" sortable) {{ simbaFormat(props.row.simba_amount) }}

</template>

<script>
import formatDate from "~/mixins/formatDate";
import formatCurrency from "~/mixins/formatCurrency";

import _ from 'lodash'
import {statusToColor} from "@/consts";

export default {
  name: "invoices",
  layout: "main",
  middleware: ["adminRequired"],
  mixins: [formatDate, formatCurrency],
  async fetch() {
    if (this.adminInvoices.length <= 0) {
      await this.$store.dispatch('invoices/fetchAdminInvoices', {q: this.searchQuery})
    }
  },
  data: () => ({
    searchQuery: '',
  }),
  computed: {
    adminInvoices() {
      return this.$store.getters["invoices/adminInvoices"];
    }
  },
  methods: {
    statusToColor,
    onSearchInput: _.debounce(function () {
      let properSearchQuery = this.searchQuery.toLowerCase().trim()

      if (properSearchQuery !== '' || properSearchQuery.length <= 0) {
        this.$store.dispatch('invoices/fetchAdminInvoices', {q: properSearchQuery})
      }
    }, 500),
    async fetchPaidInvoiced() {
      let searchQuery = this.searchQuery.toLowerCase().trim()
      await this.$store.dispatch('invoices/fetchAdminInvoices', {
        q: searchQuery,
        status: "paid",
      })
    }
  },
};
</script>

<style lang="sass" scoped>
.is-justified-between
  justify-content: space-between

</style>
