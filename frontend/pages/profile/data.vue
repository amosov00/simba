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
</template>
<script>

export default {
  name: "profile-data",
  layout: "profile",
  data: () => ({
    modalShow: false,
  }),
  computed: {
    userData() {
      return this.$store.getters.user || {}
    }
  },
  methods: {
  },
};
</script>

<style lang="sass" scoped></style>
