<template lang="pug">
  div.main-content
    h1.title.is-size-4 {{$t('su_invoices.invoices')}}
    b-table(:data="invoices" paginated per-page="30" default-sort="created_at" default-sort-direction="desc")
      template(slot-scope="props")
        b-table-column(field="created_at" label="Date" width="150" sortable) {{ timestampFromUtc(props.row.created_at) }}
        b-table-column(field="_id" label="ID" width="50" sortable)
          n-link(:to="`/invoices/${props.row._id}`") {{ props.row._id }}
        b-table-column(field="user_id" label="User ID" width="50" sortable)
          n-link(:to="`/users/${props.row.user_id}`") {{ (props.row.user_id) }}
        b-table-column(field="status" label="Status"  width="50" sortable) {{ props.row.status }}
        b-table-column(field="btc_amount" label="BTC"  width="50" sortable) {{ btcFormat(props.row.btc_amount) }}
        b-table-column(field="simba_amount" label="SIMBA"  width="50" sortable) {{ simbaFormat(props.row.simba_amount) }}

</template>

<script>
  import formatDate from "~/mixins/formatDate";
  import formatCurrency from "~/mixins/formatCurrency";

  import moment from 'moment'

  export default {
    name: "invoices",
    layout: "main",
    middleware: ["adminRequired"],
    mixins: [formatDate, formatCurrency],
    async asyncData({store}) {
      const res = await store.dispatch('invoices/fetchAdminInvoices')

      res.forEach(el => {
        el.created_at = moment(el.created_at).utc().valueOf()
      })

      return {
        invoices: res
      }
    }
  };
</script>

<style lang="scss"></style>
