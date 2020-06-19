<template lang="pug">
  div.site
    Header.header-wrapper.site-wrapper
    nuxt
    b-modal(:active.sync="showModalNew" has-modal-card)
      PasswordChange
</template>

<script>
  import Header from "~/components/Header";

  import PasswordChange from "~/components/PasswordChange";

  export default {
    middleware: ['fetchUser', 'contract'],
    components: { Header, PasswordChange },
    data: () => ({
      showModalNew: false
    }),
    created() {
      this.$on('showModalNew', () => {
        this.showModalNew = true
      })
    }
  }
</script>

<style lang="sass" scoped>
</style>
