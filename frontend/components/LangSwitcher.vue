<template lang="pug">
  div.lang-switcher
    div.lang-switcher__button(@mouseenter="showList = true" @mouseleave="showList = false" @click="showList = false")
      span.lang-switcher__lang {{ currentLanguage }}
      inline-svg(:src="require(`@/assets/images/${langList[currentLanguage]}`)").lang-switcher__flag
      div.lang-switcher__tooltip(:class="{'is-flex': showList}")
        div(v-for="(icon, lang) in otherLanguages" :key="lang" @click="$i18n.setLocale(lang)").lang-switcher__item
          span.lang-switcher__lang {{ lang }}
          inline-svg(:src="require(`@/assets/images/${icon}`)").lang-switcher__flag
    //--select.lang-switcher__select(@change="changeLocale" v-model="locale" :class="{'lang-switcher__select--sidebar': sidebar}")
      option(v-for="(val, key) in langList" :value="key" :key="key" @click="changeLocale(key)") {{ val }}
</template>

<script>
  import InlineSvg from 'vue-inline-svg'

  export default {
    name: 'LangSwitcher',

    components: {InlineSvg},

    props: {
      sidebar: Boolean,
      default: false
    },

    beforeMount() {
      this.locale = this.$i18n.locale
    },

    computed: {
      currentLanguage() {
        return this.$i18n.locale
      },

      otherLanguages() {
        let currentLocale = this.currentLanguage;

        return Object.keys(this.langList)
          .filter(key => key !== currentLocale)
          .reduce((obj, key) => {
            obj[key] = this.langList[key]
            return obj
          }, {})
      }
    },
    data: () => ({
      showList: false,
      locale: '',
      langList: {'en': 'english.svg', 'ru': 'russian.svg'}
    }),
    methods: {
      changeLocale() {
        this.$i18n.setLocale(this.locale)
      }
    }
  }
</script>

<style lang="sass">
  .lang-switcher
    display: flex
    align-items: center
    justify-content: center
    &__item
      display: flex
      align-items: center
      justify-content: space-between
      padding: 6px 13px
      &:hover
        color: #0060FF
    &__tooltip
      flex-wrap: wrap
      flex-direction: column
      display: none
      position: absolute
      left: 0
      bottom: 40px
      background: #FFFFFF
      box-shadow: 0px 16px 32px rgba(0, 0, 0, 0.12)
      border-radius: 4px
      margin-bottom: -8px
      padding: 6px 0
      &:after
        position: absolute
        content: ""
        border-top: 5px solid #ffffff
        border-right: 5px solid transparent
        border-left: 5px solid transparent
        bottom: -5px
        top: auto
        right: auto
        left: 50%
        transform: translateX(-50%)
    &__lang
      text-transform: uppercase
      font-family: Didact Gothic, Roboto, sans-serif
      font-style: normal
      font-weight: normal
      font-size: 16px
      line-height: 0
    &__flag
      width: 20px
      height: 16px
      margin-left: 10px
      position: relative
      border: 1px solid #f6f6f6
    &__button
      position: relative
      display: flex
      align-items: center
      padding: 8px 10px
      cursor: pointer
      &:hover
        background-color: #f6f6f6
        border-radius: 2px
    &__select
      margin-left: 10px
      padding: 5px 8px
      cursor: pointer
      border-radius: 4px
      &--sidebar
        position: relative
        top: 30px
        background-color: #002c60
        border: 0
        color: #ffffff
      option
        cursor: pointer
</style>
