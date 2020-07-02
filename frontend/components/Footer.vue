<template lang="pug">
  footer.the-footer
    div.the-footer__wrapper
      div.the-footer__icons-list
        a(:href="$i18n.t(`socials.${soc.id}`)" v-for="soc in socials" target="_blank" rel="noopener noreferrer").the-footer__soc-link
          InlineSvg(:src="require(`~/assets/images/socials/${soc.icon}`)").the-footer__icon
      div.the-footer__copyright © 2019–2020 SIMBA
      div.mt-1.is-flex.align-items-center
        a(href="https://simba.storage/terms-of-use.pdf" target="_blank" rel="noopener noreferrer").the-footer__link {{ $t('footer.tos') }}
        //--a(href="https://simba.storage/privacy-policy.pdf" target="_blank" rel="noopener noreferrer").the-footer__link {{ $t('footer.privacy') }}
        //--a(href="https://simba.storage/cookies-policy.pdf" target="_blank" rel="noopener noreferrer").the-footer__link {{ $t('footer.cookies') }}
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
        { id: 'facebook', icon: 'facebook.svg' },
        { id: 'bitcoin', icon: 'bitcoin.svg' },
        { id: 'instagram', icon: 'instagram.svg' },
        { id: 'medium', icon: 'medium.svg' },
        { id: 'zen', icon: 'zen.svg' },
        { id: 'reddit', icon: 'reddit.svg' },
        { id: 'twitter', icon: 'twitter.svg' },
        { id: 'vk', icon: 'vk.svg' },
        { id: 'telegram', icon: 'telegram.svg' },
        { id: 'discord', icon: 'discord.svg' },
        { id: 'telegram_chat', icon: 'telegram.svg' },
        { id: 'streemit', icon: 'streemit.svg' },
        { id: 'github', icon: 'github.svg' },
        { id: 'linkedin', icon: 'linkedin.svg' },
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
      margin-right: 33px
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
