<template lang="pug">
  footer.the-footer
    div.the-footer__wrapper
      div.the-footer__icons-list
        a(:href="soc.url" v-for="soc in socials").the-footer__soc-link
          InlineSvg(:src="require(`~/assets/images/socials/${soc.icon}`)").the-footer__icon
      div.the-footer__copyright © 2019–2020 SIMBA
      div.mt-1.is-flex.align-items-center
        a(href="https://simba.storage/terms-and-conditions" target="_blank" rel="noopener").the-footer__link Terms of Use
        a(href="#").the-footer__link Privacy Policy
        a(href="#").the-footer__link Cookies Policy
        LangSwitcher


</template>

<script>
  import LangSwitcher from "~/components/LangSwitcher";

  import InlineSvg from 'vue-inline-svg';

  export default {
    name: 'Footer',
    components: { InlineSvg, LangSwitcher },
    data: () => ({
      socials: [
        { url: '#', icon: 'facebook.svg' },
        { url: '#', icon: 'bitcoin.svg' },
        { url: '#', icon: 'instagram.svg' },
        { url: '#', icon: 'medium.svg' },
        { url: '#', icon: 'zen.svg' },
        { url: '#', icon: 'reddit.svg' },
        { url: '#', icon: 'twitter.svg' },
        { url: '#', icon: 'vk.svg' },
        { url: '#', icon: 'telegram.svg' },
        { url: '#', icon: 'discord.svg' },
        { url: '#', icon: 'streemit.svg' },
        { url: '#', icon: 'github.svg' },
      ]
    })
  }
</script>

<style lang="sass">
  .the-footer
    padding: 0 126px 0 126px
    font-size: 16px
    font-family: "Didact Gothic", "Roboto", sans-serif
    position: relative
    &__wrapper
      padding: 33px 0 43px 0
      border-top: 1px solid #E5E5E5
    &__icon
      color: #DFDFDF
      transition: 200ms color
      &:hover
        color: #000000
    &__soc-link
      width: 30px
      height: 30px
      display: flex
      align-items: center
      justify-content: center
      text-align: center
      margin-right: 40px
    &__icons-list
      display: flex
      align-items: center
      flex-wrap: wrap
    &__copyright
      margin-top: 43px
    &__link
      margin-right: 20px
      &:last-child
        margin-right: 0
</style>
