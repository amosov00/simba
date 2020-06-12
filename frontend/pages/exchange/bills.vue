<template lang="pug">
  div
    div.is-flex.content-tabs
      n-link(to="/exchange/trade" active-class="link--active").link.link--underlined.content-tabs-item Buy/sell
      n-link(to="/exchange/bills" active-class="link--active").link.link--underlined.content-tabs-item Bills
    div.main-content Bills
</template>

<script>
  export default {
    name: "exchange-bills",
    layout: 'main',
    data: () => {
      return {
      }
    }
  };
</script>

<style lang="sass" scoped>
</style>
