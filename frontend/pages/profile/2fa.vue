<template lang="pug">
  div
    div
      button.mt-4.btn(type="button" v-if="!is2fa" @click="show2faModal") {{$t('other.enable')}} 2FA
      button.mt-4.btn(type="button" v-else @click="disableConfirmation") {{$t('other.disable')}} 2FA
    div
      b-modal(:active.sync="modal2FA" has-modal-card)
        Modal2FA
</template>

<script>
  import Modal2FA from "~/components/Modal2FA";

  export default {
    name: 'profile-twofactor',
    layout: "profile",
    components: { Modal2FA },
    data: () => ({
      modal2FA: false
    }),

    computed: {
      is2fa() {
        return this.$store.getters.user.two_factor;
      }
    },

    methods: {
      show2faModal() {
        this.modal2FA = !this.modal2FA;
      },
      disableConfirmation() {
        this.$buefy.dialog.prompt({
          confirmText: this.$i18n.t('other.disable'),
          cancelText: this.$i18n.t('other.cancel'),
          inputAttrs: {
            type: "text",
            placeholder: this.$i18n.t('profile.pin_code'),
            value: "",
            maxlength: 6,
            min: 0
          },
          trapFocus: true,
          onConfirm: value => this.$store.dispatch('delete2fa', value)
        });
      }
    }
  }
</script>

<style lang="sass" scoped>
</style>
