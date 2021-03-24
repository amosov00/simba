<template lang="pug">
  div
    div.is-flex.align-items-center.columns
      div.column.is-3.has-text-grey {{$t('other.name')}}
      div.column.is-9.has-text-weight-bold.is-size-6 {{ userData.first_name }} {{ userData.last_name }}
    div.is-flex.align-items-center.columns
      div.column.is-3.has-text-grey Email
      div.column.is-9.has-text-weight-bold.is-size-6 {{ userData.email }}
    div.is-flex.align-items-center.columns
      div.column.is-3.has-text-grey Telegram
      div.column.is-9.has-text-weight-bold.is-size-6 {{ userData.telegram_id }}
    div.is-flex.align-items-center.columns
      div.column.is-3.has-text-grey {{$t('profile.identity')}}
      div.column.is-9.has-text-weight-bold.is-size-6 {{ userData.is_active ? $i18n.t('profile.email_verified') : $i18n.t('profile.email_unverified') }}
    div.is-flex.align-items-center.columns
      div.column.is-3.has-text-grey {{$t('profile.verification')}}
      div.column.is-9.has-text-weight-bold.is-size-6 {{tier}}: {{limits.btc_used / 100000000}} BTC / {{limits.btc_limit / 100000000}} BTC
        |
        nuxt-link(to="/profile/verification")  ({{ $i18n.t('profile.upgrade') }})
</template>
<script>
import { mapActions, mapState } from 'vuex'

export default {
  name: 'profile-data',
  layout: 'profile',
  middleware: ['contract'],
  data: () => ({
    modalShow: false,
  }),
  async created() {
    await this.$store.dispatch('exchange/fetchLimits')
  },
  computed: {
    ...mapState(['kyc']),
    emailConfirm() {
      return this.userData.is_active
    },
    documentReviewed() {
      return this.kyc.is_verified && this.kyc.status === 'completed'
    },
    userData() {
      return this.$store.getters.user || {}
    },
    limits() {
      return this.$store.getters['exchange/limits']
    },
    tier() {
      if (this.emailConfirm) {
        return this.$t('profile.oneTier')
      } else if (this.documentReviewed) {
        return this.$t('profile.twoTier')
      }
    },
  },
  methods: {
    ...mapActions(['getKYCStatus']),
  },
  async mounted() {
    if (_.isEmpty(this.kyc)) {
      await this.getKYCStatus()
    }
  }
}
</script>

<style lang="sass" scoped></style>
