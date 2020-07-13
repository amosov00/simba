<template lang="pug">
  div
    h3(v-if="isBuy").text-large.has-text-weight-bold {{ $t('exchange.confirm_wallet')}}
    div(v-else).is-size-6
      span.has-text-weight-bold {{$t('exchange.choose_btc_wallet.p1')}}
      = ' '
      span {{$t('exchange.choose_btc_wallet.p2')}}
    div.is-flex.mt-2.align-items-center.space-between
      div(v-if="isBuy").is-flex.align-items-center
        img(src="~assets/images/eth.svg").mr-2
        div.text-large {{ eth_address }}
        //-- img(src="~assets/images/bitcoin.svg").mr-2
      div(v-else).is-flex.align-items-center.flex-1.mr-4
        b-select(placeholder="" expanded v-model="selectedOptions").flex-1.mr-3
          option(v-for="op in user.user_btc_addresses") {{ op.address }}
        a(href="#" @click="addNewWalletModal") {{$t('wallet.add_wallet')}}
      button.btn(@click="next") {{ $t('exchange.confirm')}}
    div.mt-2.has-text-danger {{ errors[0] }}
</template>

<script>
  import AddNewWallet from "~/components/AddNewWallet";

  export default {
    name: 'trade-wallet-confirm',
    data: () => ({
      selectedOptions: '',
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
      addNewWalletModal() {
        this.$buefy.modal.open({
          parent: this,
          component: AddNewWallet,
          hasModalCard: true,
          trapFocus: true,
          props: { type: 'btc' }
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

          if(this.selectedOptions.length <= 0) {
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
</style>
