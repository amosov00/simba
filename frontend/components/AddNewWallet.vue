<template lang="pug">
  div.add-new-wallet
    div(v-if="type === 'btc'")
      div(v-if="!confirm_screen")
        div.add-new-wallet__title {{$t('wallet.add_new_wallet.p1')}} {{ type.toUpperCase() }} {{$t('wallet.add_new_wallet.p2')}}
        div
          img(:src="require('@/assets/images/bitcoin.svg')").add-new-wallet__logo
        div
          b-input(v-model="wallet" :placeholder="$i18n.t('other.address')").input--material
        //--b-field(:label="$i18n.t('wallet.pin_code')" v-if="user.two_factor && type === 'btc'")
          b-input(type="number" v-model="pin_code")
        //-- && pin_code.toString().length != 6"
        div.mt-3.add-new-wallet__btc-info By adding the BTC address of your wallet you confirm that you have entered the correct one.
        div.add-new-wallet__btc-info For total and irrevocable loss of funds when withdrawing to these address you accept the responsibility.
        div.mt-3
          button(@click="next_screen" :disabled="!wallet").btn.w-100 {{$t('other.add')}}
      div(v-else)
        div.add-new-wallet__title Security verification
        div.add-new-wallet__complete-text To confirm, please complete the verification
        input(v-model="pin_code").add-new-wallet__pin-code
        div.mt-3
          button(@click="add" :disabled="pin_code.length !== 6").btn.w-100 Confirm
    div(v-else)
      div.add-new-wallet__title {{$t('wallet.add_new_wallet.p1')}} {{ type.toUpperCase() }} {{$t('wallet.add_new_wallet.p2')}}
      div.mb-5
        img(:src="require('@/assets/images/metamask.svg')").add-new-wallet__logo
      div(v-if="!confirm_screen")
        div To add a new address,
          =' '
          nuxt-link(to="/profile/bill/").link connect
          =' '
          | your personal account to the Ethereum wallet.
        div If this is your first time, please install
          =' '
          a(href="https://metamask.io/" target="_blank" rel="noreferrer noopener").link MetaMask
          =' '
          | extension.
        div.mt-2.has-text-grey For mobile devices we recommend the
          =' '
          a(href="https://metamask.io/" target="_blank" rel="noreferrer noopener").link MetaMask
          =' '
          | or
          =' '
          a(href="https://token.im/" target="_blank" rel="noreferrer noopener").link imToken
          =' '
          | application.
        div.mt-3
          button.btn.w-100(@click="next_screen") {{$t('other.add')}}
      div.mt-3(v-if="confirm_screen")
        div.add-new-wallet__eth-wallet {{ wallet }}
        div.has-text-grey (to change the address you need to switch in the wallet)
        button.add-new-wallet__confirm-btn.btn.w-100(@click="add" :disabled="!wallet || metamask_window_opened").btn.w-100 Confirm
</template>

<script>
export default {
  name: "AddNewWallet",
  props: {
    type: String
  },
  data: () => ({
    wallet: "",
    pin_code: "",
    metamask_window_opened: false,
    confirm_screen: false,
    eth_wallet_check: null
  }),
  computed: {
    user() {
      return this.$store.getters.user;
    }
  },

  beforeDestroy() {
    clearInterval(this.eth_wallet_check)
  },

  methods: {
    check_eth_wallet() {
      this.eth_wallet_check = setInterval(() => {
        if(window.ethereum !== undefined) {
          if(this.wallet !== window.ethereum.selectedAddress) {
            this.wallet = window.ethereum.selectedAddress
          }
        }
      }, 2000)
    },

    next_screen() {
      if(this.type === 'eth') {
        if(window.ethereum !== undefined) {
          this.wallet = window.ethereum.selectedAddress
          this.confirm_screen = true
          this.check_eth_wallet()
        }
      } else {
        if(this.user.two_factor) {
          this.confirm_screen = true
        } else {
          this.add()
        }
      }
    },

    async add() {

      clearInterval(this.eth_wallet_check)

      if(this.type === 'eth') {
        this.metamask_window_opened = true
      }

      this.$store.dispatch("addAddress", {
        type: this.type,
        address: this.wallet,
        created_at: Date.now(),
        pin_code: this.pin_code
      }).then(_ => {
        if(this.type === 'eth') {
          this.metamask_window_opened = false
        }
        this.$emit('close')
      }).catch(_ => {
        if(this.type === 'eth') {
          this.metamask_window_opened = false
          this.$buefy.toast.open({message: this.$i18n.t('wallet.failed_to_get_signature'), type: 'is-danger'})
        }
      })
    }
  }
};
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
