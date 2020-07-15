<template lang="pug">
  div
    h3(v-if="isBuy").text-large.has-text-weight-bold {{ $t('exchange.confirm_wallet')}}
    div.is-flex.mt-2.align-items-center.space-between
      div(v-if="isBuy").is-flex.align-items-center
        img(src="~assets/images/eth.svg").mr-2
        div.text-large {{ eth_address }}
        //-- img(src="~assets/images/bitcoin.svg").mr-2
      div(v-else)
        div.is-size-6.mb-1
          span.has-text-weight-bold Choose ETH wallet
          = ' '
          span.has-text-grey-light to sell SIMBA
        div.is-flex.align-items-center.mr-4
          b-select(expanded v-model="selectedOptions_eth").mr-3.wallet-select
            option(v-for="op in user.user_eth_addresses") {{ op.address }}
          a(href="#" @click="addNewWalletModal('eth')") {{$t('wallet.add_wallet')}}
        div.is-size-6.mt-4.mb-1
          span.has-text-weight-bold {{$t('exchange.choose_btc_wallet.p1')}}
          = ' '
          span.has-text-grey-light {{$t('exchange.choose_btc_wallet.p2')}}
        div.is-flex.align-items-center.mr-4
          b-select(expanded v-model="selectedOptions").mr-3.wallet-select
            option(v-for="op in user.user_btc_addresses") {{ op.address }}
          a(href="#" @click="addNewWalletModal('btc')") {{$t('wallet.add_wallet')}}
        div.mt-4
          button.btn(@click="next") {{ $t('exchange.confirm')}}
      button.btn(@click="next" v-if="isBuy") {{ $t('exchange.confirm')}}
    div.mt-2.has-text-danger {{ errors[0] }}
</template>

<script>
  import AddNewWallet from "~/components/AddNewWallet";

  export default {
    name: 'trade-wallet-confirm',
    data: () => ({
      selectedOptions: '',
      selectedOptions_eth: '',
      errors: []
    }),

    components: { AddNewWallet },

    computed: {
      isBuy() {
        return this.$store.getters['exchange/tradeData']['operation'] === 1;
      },
      user() {
        return this.$store.getters['user'];
      },

      eth_address() {
        return this.$store.getters['exchange/tradeData']['eth_address']
      }
    },

    methods: {
      addNewWalletModal(type) {
        this.$buefy.modal.open({
          parent: this,
          component: AddNewWallet,
          trapFocus: true,
          props: { type }
        });
      },

      saveAddress(data) {
        this.$store.dispatch("addAddress", data).then(_ => {
          this.$parent.$emit('nextStep')
        }).catch(_ => {
          this.$buefy.toast.open({message: this.$i18n.t('wallet.failed_to_get_signature'), type: 'is-danger'})
        })
      },

      next() {

        if (this.isBuy) {

          if(this.user.user_eth_addresses.length > 0) {
            if(this.user.user_eth_addresses.find(el => el.address === this.eth_address) !== undefined) {
              this.$parent.$emit('nextStep')
              return
            }
          }

          let data = {
            type: 'eth',
            address: this.eth_address,
            created_at: Date.now(),
          }

          this.saveAddress(data)
        } else {

          this.errors = []

          if(this.selectedOptions_eth.length < 1) {
            this.errors.push('Please choose ETH wallet!')
            return
          }

          if(this.selectedOptions.length < 1) {
            this.errors.push(this.$i18n.t('exchange.choose_btc_wallet_error'))
            return
          }

          this.$store.commit('exchange/setTradeData', { prop: 'btc_redeem_wallet', value: this.selectedOptions })
          this.$parent.$emit('nextStep')
        }
      }
    }
  }
</script>

<style lang="sass">
  .wallet-select
    width: 500px
    .select
      select
        border: 1px solid rgba(0,0,0,0)
        border-bottom: 1px solid #E5E5E5
        &:focus
          border: 1px solid #0060FF
          box-shadow: none
        &:hover
          border-bottom: 1px solid #0060FF
</style>
