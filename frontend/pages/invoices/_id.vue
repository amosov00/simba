<template lang="pug">
  div.main-content
    h1.title.is-size-4 Invoices by ID — {{this.$route.params.id}}
</template>

<script>
import formatDate from "~/mixins/formatDate";
import formatCurrency from "~/mixins/formatCurrency";
export default {
  name: "invoicesById",
  layout: "main",
  middleware: ["adminRequired"],
  mixins: [formatDate, formatCurrency],
  computed: {
    invoiceById() {
      return this.$store.getters['invoice/invoiceById']
    }
  },
  created() {
    this.$store.dispatch("invoices/fetchInvoiceById", this.$route.params.id);
  }
};
</script>

<style lang="scss"></style>
