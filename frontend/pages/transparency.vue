<template lang="pug">
  div.transparency
    div.main-content
      h1.title.is-size-4 Transparency
        section.transparency__section
          img(src="../assets/images/chart.png")
      h1.title.is-size-4 Current Balances
        section.transparency__section
          img(src="../assets/images/logo-lg.png")
</template>

<script>
  export default {
    name: "transparency",
    layout: "main",
    data() {
      return {
      };
    },
    methods: {
    },
  };
</script>

<style lang="scss" scoped>
.transparency {
  &__section {
    margin-top: 50px;
    text-align: center;
  }
}
</style>
