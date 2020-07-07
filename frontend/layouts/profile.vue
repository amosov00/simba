<template lang="pug">
  div.site
    Header.header-wrapper.site-wrapper
    div.is-flex.site-wrapper.main-content.columns.m-0
      div.sidebar
        div.sidebar__inner
          div(v-for="(menu_item, i) in  sidebar" :key="i").is-size-6
            div {{ $t(menu_item.id) }}
            div.mt-2.mb-3.sidebar__links-block
              n-link(:to="link.url" v-for="(link, j) in menu_item.links" :key="j" exact-active-class="link--active").link.is-size-6.is-block {{ $t(link.id) }}
          div.mt-3.logout-block
            a(href="#" @click="logout").link {{$t('profile.sidebar.logout')}}
      nuxt.flex-1.profile-content
    Footer

</template>

<script>
  import Footer from "~/components/Footer";
  import Header from "~/components/Header";

  export default {
    middleware: ['fetchUser', 'authRequired'],
    components: { Header, Footer },
    data: () => ({
      showModalNew: false,
      sidebar: [
        { id: 'profile.sidebar.personal',
          links: [
            {id: 'profile.sidebar.data', url: '/profile/data/'},{id: 'profile.sidebar.verification', url: '/profile/verification/'}
          ]
        },
        { id: 'profile.sidebar.payment',
          links: [
            {id: 'profile.sidebar.bill_details', url: '/profile/bill/'},{id: 'profile.sidebar.partner_program', url: '/profile/partner/'}
          ]
        },
        { id: 'profile.sidebar.security',
          links: [
            {id: 'profile.sidebar.change_password', url: '/profile/change-password/'},{id: 'profile.sidebar.two_factor', url: '/profile/2fa/'}
          ]
        }
      ]
    }),
    methods: {
      logout() {
        this.$authLogout();
      },
    },
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
    &__inner
      border-right: 1px solid #E5E5E5
      min-height: 292px
      padding-right: 30px
    &__links-block
      padding-left: 20px
  .profile-content
    padding-left: 40px

</style>
