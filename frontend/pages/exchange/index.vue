<template lang="pug">
  div
    div.is-flex
      n-link(to="/exchange/buysell" active-class="link--active").link Buy/sell
      n-link(to="/exchange/bills" active-class="link--active").link Bills
</template>

<script>
  export default {
    name: "Exchange",
    layout: 'main',
  };
</script>

<style lang="sass" scoped>
</style>
