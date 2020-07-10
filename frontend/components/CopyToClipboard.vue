<template lang="pug">
  div.copy-button__wrapper
    div.copy-button(@click="copy")
      img(:src="require('~/assets/images/copy.svg')").copy-button__icon
    input(:value="value_to_copy" ref="reflink").hidden-input

</template>

<script>
  export default {
    name: 'CopyToClipboard',
    props: {
      value_to_copy: {
        default: '',
        type: String
      }
    },
    methods: {
      copy() {
        this.$refs.reflink.select();
        this.$buefy.toast.open({ message: this.$i18n.t('other.copied_to_clipboard'), type: 'is-primary' });
        document.execCommand('copy');
      }
    }
  }
</script>

<style lang="sass">
  .copy-button
    width: 36px
    height: 15px
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

  .hidden-input
    position: absolute
    left: -9999px
</style>
