<template lang="pug">
  div.site-wrapper
    div.wallet-content--hero
      h1.title.is-size-4 Transfer SIMBA tokens
      div
        b-field(label="Your wallet (selected MetaMask address)")
          b-input(size="is-small" v-model="selectedAddress" disabled)
        button.btn--inline(@click="metamaskModal" v-if="selectedAddress") add new
        b-field(label="Recipient")
          b-input(size="is-small" v-model="transferData.address")
        b-field(label="Amount")
          b-input(size="is-small" type="number" min="0" step="10000" v-model="transferData.amount")
        div.wallet-content__totals
          p.subtitle.is-size-6 Fee: 5,000 SIMBA
          p.title.is-size-6 Total: {{totalAmount}} SIMBA
            span.subtitle.is-size-6 (0 USDT / {{totalBTC}} BTC)
        button(@click="transferFunds").btn.w-100 Send SIMBA
    hr.mt-4
    div.wallet-content__table
      h1.title.is-size-4 History of transactions
      WalletTable(:moreData="moreData")
      div.wallet-content__button
        button.btn--outlined(@click="moreData += 10") more
</template>

<script>
import WalletTable from "~/components/WalletTable";
import WalletConnection from "~/components/WalletConnection";
export default {
  name: "exchange-transfer",
  layout: "main",
  middleware: ["contract", "metamask"],
  components: { WalletTable, WalletConnection },
  data: () => {
    return {
      transferData: {
        address: "",
        amount: 0
      },
      moreData: 10
    };
  },
  methods: {
    transferFunds() {
      if (this.transferData.address && this.transferData.amount > 0) {
        this.$store.dispatch("contract/transferSimbaToken", this.transferData);
      }
    },
    metamaskModal() {
      this.$buefy.modal.open({
        parent: this,
        component: WalletConnection,
        hasModalCard: true,
        trapFocus: true
      });
    }
  },
  computed: {
    selectedAddress() {
      if (window.ethereum) {
        return window.ethereum.selectedAddress;
      } else {
        return false;
      }
    },
    totalAmount() {
      return this.transferData.amount > 0
        ? this.transferData.amount * 1 + 5000
        : 0;
    },
    totalBTC() {
      return (this.transferData.amount * 1) / 100000000;
    }
  }
};
</script>

<style lang="sass" scoped>
.wallet-content
  max-width: 840px
  width: 100%
  margin: 0 216px

  &--hero
    width: 600px

  &__totals
    margin: 25px 0

  &__table
    margin-bottom: 60px

  &__button
    margin-top: 20px
    text-align: center
</style>
