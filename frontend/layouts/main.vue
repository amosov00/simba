<template lang="pug">
  div.site
    Header.header-wrapper.site-wrapper
    nuxt
</template>

<script>
  import Header from "~/components/Header";

  export default {
    components: { Header }
  }
</script>

<style lang="sass" scoped>
</style>
