<template lang="pug">
  div.card.metamask-window
    div.card-content(v-if="!isAdd")
      div.title.is-4 Add new ETH address
      div
        img(:src="require('@/assets/images/metamask.svg')")
      div.mt-2
        div To add a new address, connect your personal account to the Ethereum wallet. If this is your first time, please install MetaMask extension.
        div.mt-2 For mobile devices we recommend the TrustWallet app.
      div.mt-4
        button.btn.w-100(@click="isAdd = true") Add
    div.card-content(v-else)
      div.title.is-4 Add new ETH address
      div
        img(:src="require('@/assets/images/metamask.svg')")
      div.mt-2
        p.title.is-6 {{selectedAddress}}
        div.mt-2 (to change the address you need to switch in the wallet)
      div.mt-4
        button.btn.w-100(@click.once="signAddress") Confirm
</template>

<script>
export default {
  name: 'MetamaskWallet',
  data: () => ({
    isAdd: false,
  }),
  methods: {
    signAddress() {
      this.$store.dispatch('metamask/signAddress')
      this.$parent.close()
    },
  },
  computed: {
    selectedAddress() {
      if (window.ethereum) {
        return window.ethereum.selectedAddress
      } else {
        return false
      }
    },
  },
}
</script>

<style lang="sass" scoped>
.metamask-window
  width: 650px
  padding: 20px 40px
</style>
