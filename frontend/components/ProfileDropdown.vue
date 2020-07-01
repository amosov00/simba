<template lang="pug">
  div.profile-dropdown__wrapper
    div.profile-dropdown(:class="{'profile-dropdown--opened': showFull}" @mouseover="showFull = true" @mouseout="showFull = false" @click="showFull = false")
      div.profile-dropdown__header
        div.profile-dropdown__name-wrapper
          div.profile-dropdown__name {{ name }}
          InlineSvg(:src="require('@/assets/images/dropdown.svg')").profile-dropdown__icon
      div.profile-dropdown__content
        n-link(to="/profile/bill/").profile-dropdown__link {{$t('dropdown.bill_details')}}
        n-link(to="/profile/data/").profile-dropdown__link {{$t('dropdown.personal_data')}}
        n-link(to="/profile/2fa/").profile-dropdown__link {{$t('dropdown.security')}}
      div.profile-dropdown__footer
        a(href="#" @click="logout").profile-dropdown__logout {{$t('dropdown.logout')}}
</template>

<script>
  import InlineSvg from 'vue-inline-svg'

  export default {
    name: 'ProfileDropdown',
    props: {
      name: String
    },
    components: {InlineSvg},
    data: () => ({
      showFull: false
    }),
    methods: {
      logout() {
        this.$authLogout();
      },
    }
  }
</script>

<style lang="sass">
  .profile-dropdown
    cursor: pointer
    font-weight: 300
    font-size: 16px
    line-height: 100%
    text-align: left
    display: flex
    flex-direction: column
    border-radius: 10px
    transition: 100ms all
    margin-left: auto
    position: absolute
    right: -20px
    min-width: 140px
    &__wrapper
      position: relative
      text-align: right
      height: 36px
      margin-bottom: 6px
    &__logout
      width: 100%
      color: #0060FF
      &:hover
        color: red
    &__link
      transition: 100ms all
      color: #0060FF
      padding: 4px 20px
      margin-bottom: 2px
      &:last-child
        margin-bottom: 0
      &:hover
        background-color: #0060FF
        color: #ffffff
    &__content
      display: none
      padding: 10px 0
      flex-direction: column
      border-top: 1px solid #E5E5E5
      border-bottom: 1px solid #E5E5E5
    &__icon
      margin-left: 5px
      color: #0060FF
      bottom: 2px
      position: relative
    &__header
      padding: 13px 20px 13px 20px
    &__name
      color: #0060FF
      font-weight: bold
      font-size: 18px
      padding-bottom: 3px
    &__name-wrapper
      display: flex
      align-items: center
      border-bottom: 1px dashed #0060FF
    &__footer
      display: none
      padding: 10px 20px
    &.profile-dropdown--opened
      background: #FFFFFF
      box-shadow: -6px 6px 12px rgba(0, 0, 0, 0.12)
      & .profile-dropdown__name
        color: #8C8C8C
      & .profile-dropdown__icon
        color: #8C8C8C
      & .profile-dropdown__name-wrapper
        border-bottom: 0
      & > .profile-dropdown__content
        display: flex
      & > .profile-dropdown__footer
        display: flex
</style>
