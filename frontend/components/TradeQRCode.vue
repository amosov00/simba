<template lang="pug">
  div.qr-button__wrapper
    div.qr-button(@click="qrCodeModal")
      img(:src="require('~/assets/images/qr.svg')").qr-button__icon
</template>

<script>
import AddressQRCode from '~/components/AddressQRCode'

export default {
  name: 'TradeQRCode',
  props: {
    qrcode_value: String,
    amount: null,
  },
  components: { AddressQRCode },
  methods: {
    qrCodeModal() {
      this.$buefy.modal.open({
        parent: this,
        component: AddressQRCode,
        hasModalCard: true,
        trapFocus: true,
        props: { qrcode_value: this.qrcode_value, amount: this.amount },
      })
    },
  },
}
</script>

<style lang="sass">
.qr-button
  width: 36px
  height: 36px
  display: flex
  align-items: center
  justify-content: center
  user-select: none
  position: absolute
  top: 50%
  left: 50%
  transform: translate(-50%, -50%)
  &:before
    transition: 100ms all
    border-radius: 100px
    left: calc(50%)
    top:  calc(50% - 1px)
    position: absolute
    content: ""
    width: 36px
    height: 36px
    z-index: -1
    transform: translate(-50%, -50%)
  &:hover
    cursor: pointer
    &:before
      cursor: pointer
      background-color: #f1f1f1
  &:active
    &:before
      background-color: #e3e3e3
  &__wrapper
    position: relative
    width: 36px
    height: 15px
</style>
