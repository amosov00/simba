<template lang="pug">
  div
    h3(v-if="multi_props.op !== 'sell'").text-large.has-text-weight-bold {{ $t('exchange.confirm_wallet')}}
    div(v-else).is-size-6
      span.has-text-weight-bold Choose BTC wallet
      = ' '
      span to get coins after redeem
    div.is-flex.mt-2.align-items-center.space-between
      div(v-if="multi_props.op !== 'sell'").is-flex.align-items-center
        img(src="~assets/images/eth.svg").mr-2
        div.text-large {{ eth_address }}
        //-- img(src="~assets/images/bitcoin.svg").mr-2
      div(v-else).is-flex.align-items-center.flex-1.mr-4
        b-select(placeholder="" expanded v-model="selectedOptions").flex-1.mr-3
          option(v-for="op in user.user_btc_addresses") {{ op }}
        a(href="#" @click="addNewWalletModal") add new
      button.btn(@click="next") {{ $t('exchange.confirm')}}
    div.mt-2.has-text-danger {{ errors[0] }}
    b-modal
      AddNewWallet
</template>

<script>
  import AddNewWallet from "~/components/AddNewWallet";

  export default {
    name: 'trade-wallet-confirm',

    components: {AddNewWallet},

    props: {
      multi_props: Object
    },

    data: () => ({
      selectedOptions: '',
      errors: []
    }),

    computed: {
      user() {
        return this.$store.getters['user'];
      },

      eth_address() {
        return this.$store.getters['exchange/tradeData']['eth_address']
      }
    },

    methods: {
      addNewWalletModal() {
        this.$buefy.modal.open({
          parent: this,
          component: AddNewWallet,
          hasModalCard: true,
          trapFocus: true,
          props: { type: 'btc' }
        });
      },

      async testSell() {
        await this.$store.dispatch('contract/fetchContract');
        this.$store.dispatch('contract/redeemSimbaToken', {});
      },
      next(){

        if(this.multi_props.op === 'sell') {
          if(this.selectedOptions.length <= 0) {
            this.errors.push('Please choose Bitcoin wallet')
            return
          }

          this.$store.commit('exchange/setTradeData', { prop: 'btc_target_wallet', value: this.selectedOptions })
        }

        this.$parent.$emit('nextStep')
      }
    }
  }
</script>

<style lang="sass">
</style>
