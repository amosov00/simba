<template lang="pug">
</template>

<script>
  export default {
    name: "exchange-index",
    middleware({ redirect }) {
      redirect('/exchange/trade/')
    },
    data: () => ({
    })
  };
</script>

<style lang="sass" scoped>
</style>
