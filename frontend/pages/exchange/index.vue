<template lang="pug">
  div
    div.main-content
      div
        n-link(to="/exchange/buysell").btn.mr-2 Buy
        n-link(to="/exchange/buysell").btn.mr-2 Sell
      h3.title.is-5.mt-4 Last bills
      //= b-table(:data="data" :columns="columns" focusable striped).is-flex.mt-4.data-table
      b-table(:data="invoiceData")
        template(slot-scope="props")
          b-table-column(field="created_at" label="Date" sortable) {{ (new Date(props.row.created_at)).toLocaleString() }}
          b-table-column(field="id" label="ID")
              n-link(:to="'/exchange/' + props.row._id") {{ props.row._id }}
          b-table-column(field="simba_amount" label="SIMBA Amount") {{ props.row.simba_amount }}
          b-table-column(field="invoice_type" label="Type") {{ getType(props.row.invoice_type) }}
</template>

<script>
  export default {
    name: "exchange-index",
    layout: 'main',
    computed: {
      invoiceData() {
        return this.$store.getters['invoices/invoices'];
      }
    },
    data: () => {
      return {
        data: [
          { 'id': '#3', 'amount': '999 000 050 000', 'date': '01.06.2020', 'type': 'BUY', 'status': '1:15:47'},
          { 'id': '#2', 'amount': '999 000 050 000', 'date': '01.06.2020', 'type': 'Sell', 'status': 'Not paid' },
          { 'id': '#1', 'amount': '999 000 050 000', 'date': '01.06.2020', 'type': 'BUY', 'status': 'Paid' },
        ],
        columns: [
          { field: 'id', width: '40', }, { field: 'amount' }, { field: 'date', centered: true },
          { field: 'type' }, { field: 'status' }
        ]
      }
    },

    methods: {
      getType(type) {
        if(type ===  2){ return 'SELL'}

        return 'BUY'
      }
    },

    async fetch() {
      await this.$store.dispatch('invoices/fetchInvoices');
    }
  };
</script>

<style lang="sass" scoped>
</style>
