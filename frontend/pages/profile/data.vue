<template lang="pug">
  div
    div.is-flex.align-items-center.columns
      div.column.is-3.has-text-grey Name
      div.column.is-9.has-text-weight-bold.is-size-6 {{ userData.first_name }} {{ userData.last_name }}
    div.is-flex.align-items-center.columns
      div.column.is-3.has-text-grey Email
      div.column.is-9.has-text-weight-bold.is-size-6 {{ userData.email }}
    div.is-flex.align-items-center.columns
      div.column.is-3.has-text-grey Telegram
      div.column.is-9.has-text-weight-bold.is-size-6 {{ userData.telegram_id }}
    div.is-flex.align-items-center.columns
      div.column.is-3.has-text-grey Identify verification
      div.column.is-9.has-text-weight-bold.is-size-6 {{ userData.email_is_active ? "Email verified" : "Unverified" }}
    div
      button(@click="modalShow = true").btn Edit my profile
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
      return this.$store.getters.user
    }
  },
  methods: {
  },
  created() {
    this.$on('closeProfileUpdate', () => {
      console.log('closing modal')
      this.modalShow = false
    })
  },
  async asyncData({ store }) {
    await store.dispatch("getBtcAddress");
  }
};
</script>

<style lang="sass" scoped></style>
