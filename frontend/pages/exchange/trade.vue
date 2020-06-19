<template lang="pug">
  div
    div.is-flex.content-tabs
      n-link(to="/exchange/trade" active-class="link--active").link.link--underlined.content-tabs-item Buy/sell
      n-link(to="/exchange/bills" active-class="link--active").link.link--underlined.content-tabs-item Bills
      n-link(to="/exchange/transfer" active-class="link--active").link.link--underlined.content-tabs-item Transfer
    div.main-content
      n-link(to="/exchange/buysell").btn.mr-2 Buy
      n-link(to="/exchange/buysell").btn.mr-2 Sell
      b-table(:data="data" :columns="columns" focusable striped).is-flex.mt-4.data-table
</template>

<script>
  export default {
    name: "exchange-trade",
    layout: 'main',
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
    }
  };
</script>

<style lang="sass" scoped>
</style>
