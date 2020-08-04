<template lang="pug">
  div.main-content
    h1.title.is-size-4 {{$t('su_invoices.invoices')}}
    div.mb-3
      b-input(v-model="searchQuery" @input="onSearchInput" :placeholder="`${this.$i18n.t('other.search')}...`" icon="magnify")
    div(v-if="invoicesToView.length <= 0") {{ $t('other.search_empty_results') }}
    b-table(v-if="invoicesToView.length > 0" :data="invoicesToView" paginated per-page="20" default-sort="created_at" default-sort-direction="desc")
      template(slot-scope="props")
        b-table-column(field="created_at" :label="$i18n.t('su_invoices.created_at')" width="150" sortable) {{ timestampFromUtc(props.row.created_at) }}
        b-table-column(field="_id" label="ID" width="50" sortable)
          n-link(:to="`/invoices/${props.row._id}`") {{ props.row._id }}
        b-table-column(field="user_id" :label="$i18n.t('su_invoices.user_id')" width="50" sortable)
          n-link(:to="`/users/${props.row.user_id}`") {{ (props.row.user_id) }}
        b-table-column(field="status" :label="$i18n.t('su_invoices.status')"  width="50" sortable) {{ $t(`exchange.statuses.${props.row.status}`) }}
        b-table-column(field="btc_amount" label="BTC"  width="50" sortable) {{ btcFormat(props.row.btc_amount) }}
        b-table-column(field="simba_amount" label="SIMBA"  width="50" sortable) {{ simbaFormat(props.row.simba_amount) }}

</template>

<script>
  import formatDate from "~/mixins/formatDate";
  import formatCurrency from "~/mixins/formatCurrency";

  import moment from 'moment'
  import _ from 'lodash'

  export default {
    name: "invoices",
    layout: "main",
    middleware: ["adminRequired"],
    mixins: [formatDate, formatCurrency],

    data: () => ({
      invoicesCache: [],
      invoicesToView: [],
      searchQuery: '',
    }),

    methods: {
      onSearchInput: _.debounce(function() {
        let properSearchQuery = this.searchQuery.toLowerCase().trim()

        if(properSearchQuery !== '' || properSearchQuery.length <= 0) {
          this.invoicesToView = this.invoicesCache.filter(el => {
            for(let key in el){
              if(String(el[key]).toLowerCase().includes(properSearchQuery)) {
                return true
              }
            }
            return false
          })
        } else {
          this.invoicesToView = this.invoicesCache
        }
      }, 500)
    },

    async asyncData({store}) {
      const res = await store.dispatch('invoices/fetchAdminInvoices')

      res.forEach(el => {
        el.created_at = moment(el.created_at).utc().valueOf()
      })

      return {
        invoicesCache: res,
        invoicesToView: res
      }
    }
  };
</script>

<style lang="scss"></style>
