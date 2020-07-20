<template lang="pug">
  div.main-content
    h1.title.is-size-4 Invoices

    b-table(:data="invoices")
      template(slot-scope="props")
          b-table-column(field="date" label="Date" width="50") {{ timestampFromUtc(props.row.created_at) }}
          b-table-column(field="_id" label="ID" width="50")
            nuxt-link(:to="`/invoices/${props.row._id}`") {{ props.row._id }}
          b-table-column(field="user_id" label="User ID" width="50") {{ (props.row.user_id) }}
          b-table-column(field="status" label="Status"  width="50") {{ props.row.status }}
          b-table-column(field="btc_amount" label="Amount, BTC"  width="50") {{ btcFormat(props.row.btc_amount) }}
          b-table-column(field="simba_amount" label="Amount, SIMBA"  width="50") {{ simbaFormat(props.row.simba_amount) }}

</template>

<script>
import formatDate from "~/mixins/formatDate";
import formatCurrency from "~/mixins/formatCurrency";
export default {
  name: "invoices",
  layout: "main",
  middleware: ["adminRequired"],
  mixins: [formatDate, formatCurrency],
  computed: {
    invoices() {
      return this.$store.getters["invoices/invoices"];
    }
  },
  created() {
    this.$store.dispatch("invoices/fetchInvoices");
  }
};
</script>

<style lang="scss"></style>
