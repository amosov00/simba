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
        n-link(to="/profile/partner/").profile-dropdown__link {{$t('dropdown.partner_program')}}
        n-link(to="/profile/2fa/").profile-dropdown__link {{$t('dropdown.security')}}
        n-link(to="/invoices" v-if="user.is_superuser").profile-dropdown__link.su-link {{$t('su_invoices.invoices')}}
        n-link(to="/manual-approval" v-if="user.is_superuser").profile-dropdown__link.su-link {{ $t('su_payouts_mm.manage_payouts')}}
        n-link(to="/users" v-if="user.is_superuser").profile-dropdown__link.su-link {{$t('su_users.users')}}
        n-link(to="/xpub" v-if="user.is_superuser").profile-dropdown__link.su-link xPub
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
    computed: {
      user() {
        return this.$store.getters.user;
      }
    },
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
    font-weight: 300
    font-size: 16px
    line-height: 100%
    text-align: left
    display: flex
    flex-direction: column
    border-radius: 10px
    margin-left: auto
    position: absolute
    right: -20px
    z-index: 10
    height: 100%
    overflow: hidden
    &__wrapper
      position: relative
      text-align: left
      height: 36px
      margin-bottom: 6px
    &__logout
      width: 100%
      color: #0060FF
      &:hover
        color: red
    &__link
      position: relative
      color: #0060FF
      padding: 4px 20px
      margin-bottom: 2px
      &:last-child
        margin-bottom: 0
      &:hover
        background-color: #0060FF
        color: #ffffff
    &__content
      display: flex
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
      text-align: left
      padding: 13px 20px 13px 20px
      cursor: pointer
    &__name
      color: #0060FF
      font-weight: bold
      font-size: 18px
      padding-bottom: 3px
    &__name-wrapper
      display: flex
      align-items: center
      justify-content: space-between
      border-bottom: 1px dashed #0060FF
    &__footer
      display: none
      padding: 10px 20px
    &.profile-dropdown--opened
      height: auto
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

  .su-link
    color: #fa0000
</style>
