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
      div.column.is-4.has-text-right.pa-0
        div.balance
          img.balance__img(src="../assets/images/bitcoin-min.svg" @click="setBtc")
          img.balance__img(src="../assets/images/tether.svg" @click="setTether")
          span.balance__amount(v-if="showBtc") {{simbaFormat(btcBalance)}} BTC
          span.balance__amount(v-else-if="showTether") {{simbaFormat(tetherBalance)}} USDT
</template>

<script>
import ProfileDropdown from "~/components/ProfileDropdown";
import _ from "lodash";
import formatCurrency from "../mixins/formatCurrency";
export default {
  name: "Header",
  mixins: [formatCurrency],
  components: {
    ProfileDropdown
  },
  computed: {
    user() {
      return this.$store.getters.user;
    },
    tetherBalance() {
      return ((this.simbaBalance / 100000000) * this.btcPrice).toFixed(2);
    },
    btcBalance() {
      return (this.simbaBalance / 100000000).toFixed(2);
    }
  },
  data: () => ({
    menu: [],
    simbaBalance: 0,
    btcPrice: 0,
    showBtc: true,
    showTether: false
  }),
  methods: {
    setBtc() {
      this.showBtc = true
      this.showTether = false
    },
    setTether() {
      this.showBtc = false
      this.showTether = true
    }
  },
  async created() {
    this.menu = [
      { title: "header_menu.exchange", to: "/exchange/" },
      { title: "header_menu.about", to: "/about" },
      { title: "header_menu.howtouse", to: "/howtouse" },
      { title: "header_menu.transparency", to: "/transparency" },
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
    await this.$axios
      .get("https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD")
      .then(res => {
        this.btcPrice = res.data.USD;
      });
  }
};
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
.balance
  display: flex
  align-items: center
  justify-content: flex-end
  font-size: 18px
  &__img
    margin-right: 10px
    cursor: pointer
  &__amount
.pa-0
  padding: 0
</style>
