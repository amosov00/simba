<template lang="pug">
  div
    div.is-flex.content-tabs
      n-link(to="/exchange/trade" active-class="link--active").link.link--underlined.content-tabs-item Buy/sell
      n-link(to="/exchange/bills" active-class="link--active").link.link--underlined.content-tabs-item Bills
      n-link(to="/exchange/transfer" active-class="link--active").link.link--underlined.content-tabs-item Transfer
    div.main-content
      b-field
        b-input(size="is-small" v-model="transferData.address" placeholder="Address")
      b-field
        b-input(size="is-small" type="number" v-model="transferData.amount" placeholder="Amount")
      b-button(@click="transferFunds").btn.w-100 Transfer

</template>

<script>
export default {
  name: "exchange-transfer",
  layout: "main",
  middleware: ['contract'],
  data: () => {
    return {
      transferData: {
        address: "",
        amount: 0
      }
    };
  },
  methods: {
    transferFunds() {
      if (this.transferData.address && this.transferData.amount > 0) {
        this.$store.dispatch("contract/transferSimbaToken", this.transferData);
      }
    }
  }
};
</script>

<style lang="sass" scoped></style>
