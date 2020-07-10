<template lang="pug">
  div
    h3(v-if="isBuy").text-large.has-text-weight-bold {{ $t('exchange.confirm_wallet')}}
    div(v-else).is-size-6
      span.has-text-weight-bold Choose BTC wallet
      = ' '
      span to get coins after redeem
    div.is-flex.mt-2.align-items-center.space-between
      div(v-if="isBuy").is-flex.align-items-center
        img(src="~assets/images/eth.svg").mr-2
        div.text-large {{ eth_address }}
        //-- img(src="~assets/images/bitcoin.svg").mr-2
      div(v-else).is-flex.align-items-center.flex-1.mr-4
        b-select(placeholder="" expanded v-model="selectedOptions").flex-1.mr-3
          option(v-for="op in user.user_btc_addresses") {{ op }}
        a(href="#" @click="addNewWalletModal") add new
      button.btn(@click="next") {{ $t('exchange.confirm')}}
    div.mt-2.has-text-danger {{ errors[0] }}
</template>

<script>
  export default {
    name: 'trade-wallet-confirm',
    data: () => ({
      selectedOptions: '',
      errors: []
    }),

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
      saveAddress(data) {
        this.$store.dispatch("addAddress", data).then(_ => {
          this.$parent.$emit('nextStep')
        }).catch(_ => {
          this.$buefy.toast.open({message: this.$i18n.t('wallet.failed_to_get_signature'), type: 'is-danger'})
        })
      },

      next() {
        /*        if(this.multi_props.op === 'sell') {
                  if(this.selectedOptions.length <= 0) {
                    this.errors.push('Please choose Bitcoin wallet')
                    return
                  }

                  this.$store.commit('exchange/setTradeData', { prop: 'btc_target_wallet', value: this.selectedOptions })
                }*/

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

          /*if (this.user.two_factor) {
            this.$buefy.dialog.prompt({
              inputAttrs: {
                placeholder: this.$i18n.t('wallet.pin_code'),
                maxlength: 6
              },
              cancelText: this.$i18n.t('other.cancel'),
              confirmText: 'OK',
              trapFocus: true,
              onConfirm: (value) => {
                data['pin_code'] = value
                this.saveAddress(data)
              }
            })
          } else {
            this.saveAddress(data)
          }*/
        }

        //this.$parent.$emit('nextStep')
      }
    }
  }
</script>

<style lang="sass">
</style>
