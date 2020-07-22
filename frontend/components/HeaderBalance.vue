<template lang="pug">
  div.balance
    img.balance__img(v-if="showBtc" src="../assets/images/bitcoin-min.svg" @click="setBtc")
    img.balance__img(v-if="!showBtc" src="../assets/images/bitcoin-min-disabled.svg" @click="setBtc")
    img.balance__img(v-if="showTether" src="../assets/images/tether.svg" @click="setTether")
    img.balance__img(v-if="!showTether" src="../assets/images/tether-disabled.svg" @click="setTether")
    span.balance__amount(v-if="showBtc") {{ btcBalance }} BTC
    span.balance__amount(v-else-if="showTether") {{simbaFormat(tetherBalance)}} USDT
</template>

<script>
import formatCurrency from "../mixins/formatCurrency";
export default {
  mixins: [formatCurrency],
  props: ["simbaBalance"],
  data() {
    return {
      btcPrice: 0,
      showBtc: true,
      showTether: false
    };
  },
  methods: {
    setBtc() {
      this.showBtc = true;
      this.showTether = false;
    },
    setTether() {
      this.showBtc = false;
      this.showTether = true;
    }
  },
  computed: {
    tetherBalance() {
      return (((this.simbaBalance * 1) / 100000000) * this.btcPrice).toFixed(2);
    },
    btcBalance() {
      return ((this.simbaBalance * 1) / 100000000).toFixed(4);
    }
  },
  async created() {
    await this.$axios
      .get("https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD")
      .then(res => {
        this.btcPrice = res.data.USD;
      });
  }
};
</script>

<style lang="sass" scoped>
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
