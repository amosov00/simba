<template lang="pug">
  div
    div
      ValidationObserver(v-slot="{ handleSubmit, invalid }")
        form(@submit.prevent="handleSubmit(saveProfile)")
          div.column.is-8.p-0
            b-field(label="First name")
              ValidationProvider(mode="aggressive" rules="required|alpha_spaces|min:1" v-slot="{ errors }" name="First name")
                b-input(v-model="userData.first_name")
                span.validaton-error {{ errors[0] }}
            b-field(label="Last name")
              ValidationProvider(mode="aggressive" rules="required|alpha_spaces|min:1" v-slot="{ errors }" name="Last name")
                b-input(v-model="userData.last_name")
                span.validaton-error {{ errors[0] }}
            b-field(label="Email")
              ValidationProvider(mode="aggressive" rules="required|email" v-slot="{ errors }" name="Email")
                b-input(v-model="userData.email")
                span.validaton-error {{ errors[0] }}
            b-field(label="BTC Address")
              div {{ btc_address }}
            div.mt-3
              a.link(@click="passChangeModal = true") Change password
            button.mt-4.btn.w-100(type="button" v-if="!is2fa" @click="show2faModal") Enable 2FA
            button.mt-4.btn.w-100(type="button" v-else @click="disableConfirmation") Disable 2FA
            div.is-flex.space-between
              button.mt-4.btn(type="submit" :disabled="!changesFound || invalid") Save
              button.mt-4.btn(type="button" @click="logout") Log out
    b-modal(:active.sync="passChangeModal" has-modal-card)
      PasswordChange
    b-modal(:active.sync="modal2FA" has-modal-card)
      Modal2FA
    b-loading(is-full-page :active.sync="isLoading")
</template>

<script>
import PasswordChange from "~/components/PasswordChange";
import Modal2FA from "~/components/Modal2FA";

export default {
  name: "profile",
  layout: "profile",
  components: { PasswordChange, Modal2FA },
  computed: {
    changesFound() {
      for (let prop in this.userData) {
        if (this.userData[prop] !== this.orig_user[prop]) {
          return true;
        }
      }

      return false;
    },
    btc_address() {
      return this.$store.getters.btc_address;
    },
    is2fa() {
      return this.$store.getters.user.two_factor;
    }
  },
  data: () => ({
    isLoading: false,
    isSaveDisabled: true,
    orig_user: {},
    userData: {
      email: "",
      first_name: "",
      last_name: ""
    },
    passChangeModal: false,
    modal2FA: false
  }),
  methods: {
    async saveProfile() {
      this.isLoading = true;
      const resp = await this.$store.dispatch("changeProfile", this.userData);

      if (resp) {
        this.$buefy.toast.open({
          message: "Succesfully changed!",
          type: "is-primary"
        });
        if (!(await this.$store.dispatch("getUser"))) {
          window.location.reload(true);
        }
      } else {
        this.$buefy.toast.open({
          message: "Error changing profile!",
          type: "is-danger"
        });
      }
      this.isLoading = false;
    },
    logout() {
      this.$authLogout();
    },
    show2faModal() {
      this.modal2FA = !this.modal2FA;
    },
    disableConfirmation() {
      this.$buefy.dialog.prompt({
        message: `To confirm your action enter 2fa pin code`,
        inputAttrs: {
          type: "number",
          placeholder: "Type your pin code",
          value: "",
          maxlength: 6,
          min: 0
        },
        trapFocus: true,
        onConfirm: value => this.$store.dispatch('delete2fa', value)
      });
    }
  },
  mounted() {
    let { email, last_name, first_name } = this.$store.getters.user;

    this.userData.email = email;
    this.userData.first_name = first_name;
    this.userData.last_name = last_name;

    this.orig_user = Object.assign({}, this.userData);
  },
  async asyncData({ store }) {
    await store.dispatch("getBtcAddress");
  }
};
</script>

<style lang="sass" scoped></style>
