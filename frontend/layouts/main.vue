<template lang="pug">
  div.site
    Header.header-wrapper.site-wrapper
    nuxt
    Footer
</template>

<script>
  import Header from "~/components/Header";
  import Footer from "~/components/Footer";

  export default {
    middleware: ['fetchUser'],
    components: { Header, Footer },

    data: () => ({
    }),
  }
</script>

<style lang="sass" scoped>
</style>
