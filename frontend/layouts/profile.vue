<template lang="pug">
  div.site
    Header.header-wrapper.site-wrapper
    div.is-flex.site-wrapper.main-content.columns
      div.sidebar
        div.sidebar__inner
          div(v-for="(menu_item, i) in  sidebar" :key="i").is-size-6
            div {{ menu_item.title }}
            div.mt-2.mb-3.sidebar__links-block
              n-link(:to="link.url" v-for="(link, j) in menu_item.links" :key="j" exact-active-class="link--active").link.is-size-6.is-block {{ link.name }}
          div.mt-3.logout-block
            a(href="#").link Logout
      nuxt.flex-1.profile-content
    b-modal(:active.sync="showModalNew" has-modal-card)
      PasswordChange
</template>

<script>
  import Header from "~/components/Header";

  import PasswordChange from "~/components/PasswordChange";

  export default {
    middleware: ['fetchUser'],
    components: { Header, PasswordChange },
    data: () => ({
      showModalNew: false,
      sidebar: [
        { title: 'Personal', links: [{name: 'Data', url: '/profile/data/'},{name: 'Verification', url: '/profile/verification/'}]},
        { title: 'Payment', links: [{name: 'Bill details', url: '/profile/bill/'},{name: 'Partner program', url: '/profile/partner/'}]},
        { title: 'Security', links: [{name: 'Change password', url: '/profile/change-password/'},{name: 'Two-Factor Auth', url: '/profile/2fa/'}]}
      ]
    }),
    created() {
      this.$on('showModalNew', () => {
        this.showModalNew = true
      })
    }
  }
</script>

<style lang="sass" scoped>
  .logout-block
    padding-top: 20px
    position: relative
    &:before
      content: ""
      top: 0
      left: 0
      position: absolute
      width: 71px
      background-color: #E5E5E5
      height: 1px

  .sidebar
    width: 190px
    &__inner
      border-right: 1px solid #E5E5E5
      min-height: 292px
    &__links-block
      padding-left: 20px
  .profile-content
    padding-left: 40px

</style>
