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
        ProfileDropdown(:name="`${user.first_name} ${user.last_name}`")
        div.has-text-weight-bold.text-large {{simbaFormat(simbaBalance)}} SIMBA
    div.header-menu.columns.is-flex(v-if="user")
      div.column.is-8
        nuxt-link(:to="menuItem.to" v-for="(menuItem, i) in menu" :key="i" active-class="link--active").menu-item.link {{ $t(menuItem.title) }}
        a(href="https://simba.storage/transparency" target="_blank" rel="noopener noreferrer").menu-item.link {{$t('header_menu.transparency')}}
      div.column.is-4.has-text-right.pa-0
        HeaderBalance(:simbaBalance="simbaBalance")
</template>

<script>
import ProfileDropdown from "~/components/ProfileDropdown";
import HeaderBalance from "~/components/HeaderBalance";
import _ from "lodash";
import formatCurrency from "../mixins/formatCurrency";
export default {
  name: "Header",
  mixins: [formatCurrency],
  components: {
    ProfileDropdown,
    HeaderBalance
  },
  computed: {
    user() {
      return this.$store.getters.user;
    }
  },
  data: () => ({
    menu: [],
    simbaBalance: 0
  }),
  async created() {
    this.menu = [
      { title: "header_menu.exchange", to: "/exchange/" },
      { title: "header_menu.about", to: "/about" },
      { title: "header_menu.howtouse", to: "/howtouse" },
      { title: "header_menu.wallet", to: "/wallet" },
      { title: "header_menu.contacts", to: "/contacts" }
    ];

    if (this.$cookies.get("token")) {
      if (_.isEmpty(this.$store.getters["contract/SIMBA"])) {
        await this.$store.dispatch("contract/fetchContract");
      }
      const isUnlocked = await window.ethereum._metamask.isUnlocked();
      if (window.ethereum && isUnlocked) {
        this.$contract()
          .SIMBA.methods.balanceOf(window.ethereum.selectedAddress)
          .call()
          .then(res => {
            this.simbaBalance = res;
          });
      }
    }
  }
};
</script>

<style lang="sass">
.header
  padding-top: 40px
  padding-bottom: 14px
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
</style>
