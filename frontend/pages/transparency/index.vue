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
            li.list__item(v-for="(total, i) in simbaTotals" :key="i")
              span.list__item--name {{total.name}}
              span.list__item--value {{total.value}}
          img(src="../../assets/images/bitcoin-lg.svg")
          List.mt-3
            li.list__item(v-for="(total, i) in btcTotals" :key="i")
              span.list__item--name {{total.name}}
              span.list__item--value {{total.value}}
</template>

<script>
import List from "~/components/List";
export default {
  name: "transparency",
  layout: "main",
  components: {
    List
  },
  data() {
    return {
      simbaTotals: [
        {
          name: "Total Assets: ",
          value: "500,000,000 SIMBA"
        },
        {
          name: "Total USD equivalent: ",
          value: "50,000.78 SIMBA"
        },
        {
          name: "Issued: ",
          value: "850,000,000 SIMBA"
        },
        {
          name: "Redeemed: ",
          value: "350,000,000 SIMBA"
        },
        {
          name: "Quarantined: ",
          value: "10,000,000 SIMBA"
        },
        {
          name: "Circulation: ",
          value: "490,000,000 SIMBA"
        },
        {
          name: "SIMBA holders: ",
          value: "574"
        },
        {
          name: "Ethereum Contract: ",
          value:
            "SIMBA Stablecoin (SIMBA)0x7806a1b2b6056cda57d3e889a9513615733e2b"
        }
      ],
      btcTotals: [
        {
          name: "Total Assets: ",
          value: "14,847.8056 BTC"
        },
        {
          name: "Received: ",
          value: "18,357.9056 BTC"
        },
        {
          name: "Paid out: ",
          value: "3,510.1000 BTC"
        },
        {
          name: "Liechtenstein: ",
          value: " 3,012.0051 BTC"
        },
        {
          name: "UAE: ",
          value: "1,531.8001 BTC"
        },
        {
          name: "New Zealand: ",
          value: "8,152.0002 BTC"
        },
        {
          name: "Switzerland: ",
          value: "2,152.0002 BTC"
        }
      ]
    };
  },
  methods: {}
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
