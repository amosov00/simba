<template lang="pug">
  div.transparency
    div.main-content
      h1.title.is-size-4 Transparency
        section.transparency__section
          img(src="../../assets/images/chart.png")
      h1.title.is-size-4 Current Balances
        section.transparency__section
          img(src="../../assets/images/logo-lg.png")
          List.mt-3
            li.list__item
              span.list__item--name Total Assets:
              span.list__item--value.blue {{totalAssets}} SIMBA
            li.list__item
              span.list__item--name Total USD equivalent:
              span.list__item--value 50,000.78 USDT
            li.list__item
              span.list__item--name Issued:
              span.list__item--value 850,000,000 SIMBA
            li.list__item
              span.list__item--name Redeemed:
              span.list__item--value 350,000,000 SIMBA
            li.list__item
              span.list__item--name Quarantined:
              span.list__item--value 10,000,000 SIMBA
            li.list__item
              span.list__item--name Circulation:
              span.list__item--value 490,000,000 SIMBA
            li.list__item
              span.list__item--name SIMBA holders:
              span.list__item--value.blue 574
            li.list__item
              span.list__item--name Ethereum Contract:
              a.list__item--value.blue(href="https://rinkeby.etherscan.io/address/0x60e1bf648580aafbff6c1bc122bb1ae6be7c1352" rel="nofollow noopener" target="_blank") SIMBA Stablecoin (SIMBA) 0x7806a1b2b6056cda57d3e889a9513615733e2b66
          img(src="../../assets/images/bitcoin-lg.svg")
          List.mt-3
            li.list__item
              span.list__item--name Total Assets:
              span.list__item--value 14,847.8056 BTC
            li.list__item
              span.list__item--name Received:
              nuxt-link.list__item--value(to="/transparency/btc-recieved") 18,357.9056 BTC
            li.list__item
              span.list__item--name Paid out:
              nuxt-link.list__item--value(to="/transparency/btc-paid-out") 3,510.1000 BTC
            li.list__item
              span.list__item--name Liechtenstein:
              span.list__item--value  3,012.0051 BTC
            li.list__item
              span.list__item--name UAE:
              span.list__item--value  1,531.8001 BTC
            li.list__item
              span.list__item--name New Zealand:
              span.list__item--value  8,152.0002 BTC
            li.list__item
              span.list__item--name Switzerland:
              span.list__item--value  2,152.0002 BTC
</template>

<script>
import List from "~/components/List";
export default {
  name: "transparency",
  layout: "main",
  middleware: ["contract"],
  components: {
    List
  },
  data() {
    return {
      totalAssets: 0
    };
  },
  created() {
    this.$contract()
      .SIMBA.methods.totalSupply()
      .call()
      .then(res => {
        this.totalAssets = res;
        return;
      });
  }
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
