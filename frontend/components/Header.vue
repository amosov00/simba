<template lang="pug">
  header.header
    div.columns.is-flex.align-items-center.mb-zero
      div.column.is-5
        n-link(to='/exchange/').is-flex.align-items-center.logo-link
          img.logo(src="~/assets/images/SIMBA.svg")
          div
            div.logo-text SIMBA
            div.logo-subtext Swiss Quality Stablecoin
      div.column.is-7.has-text-right(v-if="user")
        ProfileDropdown(:name="`${user.first_name} ${user.last_name}`")
        div.has-text-weight-bold.text-large {{simbaFormat(simbaBalance)}} SIMBA
    div.header-menu.columns.is-flex(v-if="user")
      div(style="padding-left: 102px").column.is-8.pa-0
        nuxt-link(:to="menuItem.to" v-for="(menuItem, i) in menu" :key="i" active-class="link--active").menu-item.link {{ $t(menuItem.title) }}
        a(href="https://simba.storage/transparency" target="_blank" rel="noopener noreferrer").menu-item.link {{$t('header_menu.transparency')}}
      div.column.is-4.has-text-right.pa-0
        HeaderBalance(:simbaBalance="simbaBalance")
</template>

<script>
import { mapGetters } from 'vuex'
import ProfileDropdown from '~/components/ProfileDropdown'
import HeaderBalance from '~/components/HeaderBalance'
import formatCurrency from '../mixins/formatCurrency'

export default {
  name: 'Header',
  mixins: [formatCurrency],
  components: {
    ProfileDropdown,
    HeaderBalance,
  },
  data: () => ({
    menu: [
      { title: 'header_menu.exchange', to: '/exchange/' },
      { title: 'header_menu.about', to: '/about' },
      { title: 'header_menu.wallet', to: '/wallet' },
    ],
  }),
  computed: {
    ...mapGetters(['user']),
    ...mapGetters('contract', ['simbaBalance']),
  },
}
</script>

<style lang="sass" scoped>
.header
  padding-top: 40px
  padding-bottom: 14px

.logo-link
  color: #000000
  transition: 300ms opacity

  &:hover
    opacity: 0.7

  &:active
    opacity: 1

.logo
  margin-right: 20px
  height: 70px
  width: 70px

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

.balance
  display: flex
  align-items: center
  justify-content: flex-end
  font-size: 18px

  &__img
    margin-right: 10px
    cursor: pointer

.pa-0
  padding-top: 0
  padding-bottom: 0
</style>
