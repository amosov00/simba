<template lang="pug">
  div.transparency
    div.main-content
      h1.title.is-size-4 {{$t('header_menu.transparency')}}
        //- section.transparency__section
          img(src="../../assets/images/chart.png")
      h3.title.is-size-5 {{ $t('transparency.curr_balances')}}
        section.transparency__section
          img(src="../../assets/images/logo-lg.png")
          List.mt-3
            li.list__item
              span.list__item--name Total Assets:
              a(href="https://etherscan.io/token/0x7806a1b2b6056cda57d3e889a9513615733e2b66" target="_blank" rel="noopener").list__item--value.blue {{simbaFormat(totalAssets)}} SIMBA
            li.list__item
              span.list__item--name Total USD equivalent:
              span.list__item--value {{simbaFormat(totalEquivalent)}} USDT
            li.list__item
              span.list__item--name Issued:
              span.list__item--value {{simbaFormat(issued)}} SIMBA
            li.list__item
              span.list__item--name Redeemed:
              span.list__item--value {{simbaFormat(redeemed)}} SIMBA
            li.list__item
              span.list__item--name Quarantined:
              span.list__item--value {{simbaFormat(quarantined)}} SIMBA
            li.list__item
              span.list__item--name Circulation:
              span.list__item--value {{simbaFormat(circulation)}} SIMBA
            li.list__item
              span.list__item--name SIMBA holders:
              a(href="https://etherscan.io/token/0x7806a1b2b6056cda57d3e889a9513615733e2b66" target="_blank" rel="noopener").list__item--value.blue {{holders}}
            li.list__item
              span.list__item--name Ethereum Contract:
              a(href="https://etherscan.io/address/0x7806a1b2b6056cda57d3e889a9513615733e2b66" target="_blank" rel="noopener").list__item--value.blue SIMBA Stablecoin (SIMBA) 0x7806a1b2b6056cda57d3e889a9513615733e2b66
          img(src="../../assets/images/bitcoin-lg.svg")
          List.mt-3
            li.list__item
              span.list__item--name Total Assets:
              span.list__item--value 0 BTC
            li.list__item
              span.list__item--name Received:
              span.list__item--value 0 BTC
              //- nuxt-link.list__item--value(to="/transparency/btc-recieved") 0 BTC
            li.list__item
              span.list__item--name Paid out:
              span.list__item--value 0 BTC
              //- nuxt-link.list__item--value(to="/transparency/btc-paid-out") 0 BTC
            li.list__item
              span.list__item--name Liechtenstein:
              span.list__item--value  0 BTC
            li.list__item
              span.list__item--name UAE:
              span.list__item--value  0 BTC
            li.list__item
              span.list__item--name New Zealand:
              span.list__item--value  0 BTC
            li.list__item
              span.list__item--name Switzerland:
              span.list__item--value  0 BTC
</template>

<script>
import List from "~/components/List";
import formatCurrency from "~/mixins/formatCurrency";
export default {
  name: "transparency",
  layout: "main",
  middleware: ["contract"],
  mixins: [formatCurrency],
  components: {
    List
  },
  data() {
    return {
      totalAssets: 0,
      totalEquivalent: 0,
      issued: 0,
      redeemed: 0,
      quarantined: 0,
      holders: 0,
      circulation: 0
    };
  },
  async created() {
    await this.$contract().SIMBA.getPastEvents(
      "Transfer",
      {
        fromBlock: 0,
        toBlock: "latest"
      },
      (err, events) => {
        this.holders = [...new Set(events.map(item => item.returnValues.to))].length;
      }
    );
    await this.$contract().SIMBA.getPastEvents(
      "BlacklistedRemoved",
      {
        fromBlock: 0,
        toBlock: "latest"
      },
      (err, events) => {
        this.quarantined = events.length;
      }
    );
    await this.$contract().SIMBA.getPastEvents(
      "OnIssued",
      {
        fromBlock: 0,
        toBlock: "latest"
      },
      (err, events) => {
        this.issued = events.reduce((total, el) => {
          return total + el.returnValues.value * 1;
        }, 0);
      }
    );
    await this.$contract().SIMBA.getPastEvents(
      "OnRedeemed",
      {
        fromBlock: 0,
        toBlock: "latest"
      },
      (err, events) => {
        this.redeemed = events.reduce((total, el) => {
          return total + el.returnValues.value * 1;
        }, 0);
      }
    );
    await this.$contract()
      .SIMBA.methods.totalSupply()
      .call()
      .then(res => {
        this.totalAssets = res;
        return;
      });
    this.circulation = this.issued - this.redeemed - this.quarantined
    await this.$axios
      .get("https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD")
      .then(res => {
        this.totalEquivalent = (
          ((this.totalAssets * 1) / 100000000) *
          res.data.USD
        ).toFixed(2);
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
