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
    div
      button(@click="modalShow = true").btn {{ $t('profile.edit_my_profile')}}
    b-modal(:active.sync="modalShow" has-modal-card @close="modalShow = false")
      ProfileUpdate
</template>

<script>

import ProfileUpdate from "~/components/ProfileUpdate";

export default {
  name: "profile-data",
  layout: "profile",
  components: { ProfileUpdate },
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
  created() {

    this.$on('closeProfileUpdate', () => {
      this.modalShow = false
    })
  },
};
</script>

<style lang="sass" scoped></style>
