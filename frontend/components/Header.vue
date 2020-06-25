<template lang="pug">
  header.header
    div.columns.is-flex.align-items-center.mb-zero
      div.column.is-6.is-flex.align-items-center
        n-link(to='/')
          img.logo(src="~/assets/images/SIMBA.svg")
        div
          div.logo-text SIMBA
          div.logo-subtext Swiss Quality Stablecoin
      div.column.is-6.has-text-right(v-if="user")
        div.mb-1.text-large
          nuxt-link(to="/profile").link {{ user.first_name }} {{ user.last_name }}
        div.has-text-weight-bold.text-large 999 000 050 000 SIMBA
    div.header-menu.columns.is-flex(v-if="user")
      div.column.is-8
        nuxt-link(:to="menuItem.to" v-for="(menuItem, i) in menu" :key="i" active-class="link--active").menu-item.link {{ menuItem.title }}
      div.column.is-4.text-large.has-text-right 1 Bitcoin = 100 000 000 SIMBA
</template>

<script>
  export default {
    name: 'Header',
    computed: {
      user() {
        return this.$store.getters.user;
      }
    },
    data: () => ({
      menu: [
          { title: 'Exchange', to: '/exchange/' }, { title: 'About', to: '/about' }, { title: 'How to use', to: '/howtouse' },
          { title: 'Transparency', to: '/transparency' }, { title: 'Wallet', to: '/wallet' }, { title: 'Contacts', to: '/contacts' }
        ]
    })
  }
</script>

<style lang="sass">
.header
  padding-top: 40px
  padding-bottom: 14px
.logo
  margin-right: 20px
.logo-text
  font-weight: bold
  font-size: 22px
  line-height: 100%
  letter-spacing: 0.1em
  color: #000000
.logo-subtext
  margin-top: 3px
  font-weight: 300
  font-size: 18px
  line-height: 100%
.header-menu
  padding: 7px 0 7px 0
.menu-item
  font-size: 16px
  margin-right: 10px
  &:last-child
    margin-right: 0
</style>
