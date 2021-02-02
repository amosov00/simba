<template lang="pug">
  div.main-content
    div.wallet-content--hero
      h1.title.is-size-4 {{ $t('wallet.transfer_simba') }}
      div
        div.wallet-field
          div.wallet-field__label {{ $t('wallet.your_wallet') }}
          div.wallet-field__body
            b-field
              b-input(size="is-small" v-model="selectedAddress" disabled)
          div.wallet-field__action
            a(href="#" @click="metamaskModal" v-if="selectedAddress").link {{$t('wallet.add_wallet')}}
        div.wallet-field
          div.wallet-field__label {{ $t('wallet.recipient') }}
          div.wallet-field__body
            b-field
              b-input(size="is-small" v-model="transferData.address").input--material
          div.wallet-field__action
            //--a(href="#").link save address
        div.wallet-field
          div.wallet-field__label {{ $t('other.amount') }}
          div.wallet-field__body
            b-field
              b-input(size="is-small" type="number" min="0" step="10000" v-model="transferData.amount").input--material
        div.wallet-content__totals
          div.wallet-content__fee {{ $t('other.fee') }}: 5,000 SIMBA
          div.is-size-6.has-text-weight-bold {{ $t('other.total') }}: {{totalAmount}} SIMBA
            =' '
            span.subtitle.is-size-6.has-text-grey ({{totalUSDT}} USDT / {{totalBTC}} BTC)
        div.wallet-content__btn-wrap
          button(@click="transferFunds").btn.w-100 {{ $t('other.send') }} SIMBA
    hr.mt-4
    div
      h1.title.is-size-4 {{ $t('wallet.txs_history') }}
      WalletTable
</template>

<script>
import WalletTable from "~/components/WalletTable";
import AddNewWallet from "~/components/AddNewWallet";

export default {
  name: "exchange-transfer",
  layout: "main",
  middleware: ["contract", "metamask"],
  components: { WalletTable, AddNewWallet },
  data: () => {
    return {
      transferData: {
        address: "",
        amount: 0
      },
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
        component: AddNewWallet,
        trapFocus: true,
        props: { type: 'eth' }
      });
    }
  },

  async asyncData({$axios}) {
    let btc_to_usdt = await $axios
      .get("https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USDT")
      .then(res => res.data.USDT);

    return { btc_to_usdt }
  },

  computed: {
    selectedAddress() {
      if (window.ethereum) {
        return window.ethereum.selectedAddress;
      } else {
        return '';
      }
    },
    totalAmount() {
      return this.transferData.amount > 0
        ? this.transferData.amount * 1 + 5000
        : 0;
    },
    totalUSDT() {
      return (this.totalBTC * this.btc_to_usdt).toFixed(2)
    },
    totalBTC() {
      return (this.transferData.amount * 1) / 100000000;
    }
  }
};
</script>

<style lang="sass" scoped>
.wallet-field
  display: flex
  align-items: center
  margin-bottom: 20px
  &__label
    text-align: right
    width: 16%
    margin-right: 15px
    font-size: 14px
    line-height: 100%
    color: #8C8C8C
  &__body
    width: 384px
  &__action
    width: 71px
    font-size: 12px
    margin-left: 10px



.wallet-content
  width: 100%
  &__fee
    font-weight: 300
    font-size: 12px
    line-height: 100%
    color: #8C8C8C
    margin-bottom: 12px

  &__btn-wrap
    padding-right: 85px

  &--hero
    width: 574px

  &__totals
    padding-left: 107px
    margin: 25px 0
</style>
