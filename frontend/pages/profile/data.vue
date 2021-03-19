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
      div.column.is-9.has-text-weight-bold.is-size-6 {{tier}}: {{limits.btc_used}} BTC / {{limits.btc_limit}} BTC
</template>
<script>
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
    userData() {
      return this.$store.getters.user || {}
    },
    limits() {
      return this.$store.getters['exchange/limits']
    },
    tier() {
      if (this.limits.btc_limit === 0.1) {
        return this.$t('profile.oneTier')
      } else if (this.limits.btc_limit === 2) {
        return this.$t('profile.twoTier')
      }
    }
  },
  methods: {},
}
</script>

<style lang="sass" scoped></style>
