<template lang="pug">
  div.add-new-wallet
    div(v-if="type === 'btc'")
      div(v-if="!confirm_screen")
        div.add-new-wallet__title {{$t('wallet.add_new_wallet.p1')}} {{ type.toUpperCase() }} {{$t('wallet.add_new_wallet.p2')}}
        div
          img(:src="require('@/assets/images/bitcoin.svg')").add-new-wallet__logo
        div
          b-input(v-model="wallet" :placeholder="$i18n.t('other.address')").input--material
        div.mt-3.add-new-wallet__btc-info {{$t('wallet.new_btc_wallet_instruct.text0')}}
        div.mt-3.add-new-wallet__btc-info {{$t('wallet.new_btc_wallet_instruct.text1')}}
        div.mt-1.add-new-wallet__btc-info {{$t('wallet.new_btc_wallet_instruct.text2')}}
        div.mt-3
          button(@click="next_screen" :disabled="!wallet").btn.w-100 {{$t('other.add')}}
      div(v-else)
        div.add-new-wallet__title {{$t('wallet.security_verification')}}
        div.add-new-wallet__complete-text {{$t('wallet.confirm_verification')}}
        input(v-model="pin_code" maxlength="6").add-new-wallet__pin-code
        div.mt-3
          button(@click="add" :disabled="pin_code.length !== 6").btn.w-100 {{$t('exchange.confirm')}}
    div(v-else)
      div.add-new-wallet__title {{$t('wallet.add_new_wallet.p1')}} {{ type.toUpperCase() }} {{$t('wallet.add_new_wallet.p2')}}
      div.mb-5
        img(:src="require('@/assets/images/metamask.svg')").add-new-wallet__logo
      div(v-if="!confirm_screen")
        div {{ $t('wallet.new_eth_wallet_instruct.text1') }}
        div(v-html="$t('wallet.new_eth_wallet_instruct.text2', {metamask: \"<a href='https://metamask.io/' target='_blank' rel='noreferrer noopener' class='link'>MetaMask</a>\"})")
        div.mt-2.has-text-grey(v-html="$t('wallet.new_eth_wallet_instruct.text3', {metamask: \"<a href='https://metamask.io/' target='_blank' rel='noreferrer noopener' class='link'>MetaMask</a>\", imtoken: \"<a href='https://token.im/' target='_blank' rel='noreferrer noopener' class='link'>imToken</a>\"})")
        div.mt-3
          button.btn.w-100(@click="next_screen") {{$t('other.add')}}
      div.mt-3(v-if="confirm_screen")
        div.add-new-wallet__eth-wallet {{ wallet }}
        div.has-text-grey ({{$t('wallet.eth_wallet_switch_info')}})
        button.add-new-wallet__confirm-btn.btn.w-100(@click="add" :disabled="!wallet || metamask_window_opened").btn.w-100 {{$t('exchange.confirm')}}
</template>

<script>
import {mapGetters, mapActions} from 'vuex';

export default {
  name: 'AddNewWallet',
  props: {
    type: String,
  },
  data: () => ({
    wallet: '',
    pin_code: '',
    metamask_window_opened: false,
    confirm_screen: false,
  }),
  computed: {
    ...mapGetters(["user"]),
  },

  methods: {
    ...mapActions(["addAddress"]),
    next_screen() {
      if (this.type === 'eth') {
        if (window.ethereum !== undefined) {
          this.wallet = window.ethereum.selectedAddress
          this.confirm_screen = true

          window.ethereum.on('accountsChanged', (accounts) => {
            this.$nextTick(() => {
              this.wallet = accounts[0]
            })
          })
        }
      } else {
        if (this.addressExists(this.wallet, this.type)) {
          this.$buefy.toast.open({ message: this.$i18n.t('wallet.address_exist'), type: 'is-danger' })
          return
        }

        if (this.user.two_factor) {
          this.confirm_screen = true
        } else {
          this.add()
        }
      }
    },

    addressExists(address, type) {
      return this.user[`user_${type}_addresses`].map((el) => el.address).indexOf(address) !== -1
    },

    async add() {
      if (this.addressExists(this.wallet, this.type)) {
        this.$buefy.toast.open({ message: this.$i18n.t('wallet.address_exist'), type: 'is-danger' })
        return
      }

      if (this.type === 'eth') {
        this.metamask_window_opened = true
      }

      this.addAddress({
          type: this.type,
          address: this.wallet,
          created_at: Date.now(),
          pin_code: this.pin_code,
        })
        .then((_) => {
          if (this.type === 'eth') {
            this.metamask_window_opened = false
          }
          this.$emit('close')
        })
        .catch((_) => {
          if (this.type === 'eth') {
            this.metamask_window_opened = false
            this.$buefy.toast.open({ message: this.$i18n.t('wallet.failed_to_get_signature'), type: 'is-danger' })
          }
        })
    },
  },
}
</script>

<style lang="sass" scoped>
.add-new-wallet
  background: #ffffff
  max-width: 647px
  padding: 40px 73px
  margin: auto
  &__eth-wallet
    font-size: 18px
    color: #000000
  &__confirm-btn
    margin-top: 54px
  &__title
    font-size: 18px
    font-weight: 600
  &__logo
    margin-top: 41px
  &__btc-info
    line-height: 100%
    color: #8C8C8C
  &__complete-text
    margin: 40px 0
    color: #8C8C8C
  &__pin-code
    border: 0
    border-bottom: 1px solid #969696
    text-align: center
    letter-spacing: 20px!important
    font-size: 48px
    line-height: 100%
    color: #000000
    width: 100%
    &:focus
      outline: none
      border-bottom: 1px solid #0060FF
</style>
