<template lang="pug">
  div
    div.main-content
      div
        div.title.is-4 Invoice {{ invoice._id }}
      div.mt-2 Created: {{ (new Date(invoice.created_at).toLocaleString()) }}
      div.mt-1 Type: {{ getType(invoice.invoice_type) }}
      div.mt-1 Status: {{ invoice.status }}
      div.mt-4
        n-link(to="/exchange/") Go back
</template>

<script>
  export default {
    name: "invoice-by-id",
    layout: 'main',

    methods: {
      getType(type) {
        if(type ===  2){ return 'SELL'}

        return 'BUY'
      }
    },

    data: () => {
      return {
      }
    },
    async asyncData({ params, store }) {
      console.log(params)

      let data = await store.dispatch('invoices/fetchSingle', params['invoice'])

      console.log(data);

      return { invoice: data };
    }

  };
</script>

<style lang="sass" scoped>
</style>
