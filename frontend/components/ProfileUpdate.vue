<template lang="pug">
  div.card
    ValidationObserver(v-slot="{ handleSubmit, invalid }" tag="div")
      form(@submit.prevent="handleSubmit(saveProfile)" style="width: 320px").card-content
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
        div.is-flex.space-between
          b-button.mt-4.btn(:loading="isLoading" native-type="submit" :disabled="!changesFound || invalid") Save
</template>

<script>
  import WalletConnection from "~/components/WalletConnection";

  export default {
    name: "ProfileUpdate",
    computed: {
      changesFound() {
        for (let prop in this.userData) {
          if (this.userData[prop] !== this.orig_user[prop]) {
            return true;
          }
        }

        return false;
      },
    },
    data: () => ({
      isLoading: false,
      isSaveDisabled: true,
      orig_user: {},
      userData: {
        email: "",
        first_name: "",
        last_name: ""
      }
    }),
    methods: {
      async saveProfile() {
        this.isLoading = true;


        let data_to_send = {};

        for (let prop in this.userData) {
          if (this.userData[prop] !== this.orig_user[prop]) {
            data_to_send[prop] = this.userData[prop]
          }
        }

        const resp = await this.$store.dispatch("changeProfile", data_to_send);

        if (resp) {
          this.$buefy.toast.open({
            message: "Succesfully changed!",
            type: "is-primary"
          });
          /*if (!(await this.$store.dispatch("getUser"))) {
            window.location.reload(true);
          }*/
          await this.$store.dispatch("getUser");
        } else {
          this.$buefy.toast.open({
            message: "Error changing profile!",
            type: "is-danger"
          });
        }
        this.$parent.$emit('close')
        this.isLoading = false;
      },
    },
    mounted() {
      let { email, last_name, first_name } = this.$store.getters.user;

      this.userData.email = email;
      this.userData.first_name = first_name;
      this.userData.last_name = last_name;

      this.orig_user = Object.assign({}, this.userData);
    },
  };
</script>

<style lang="sass" scoped></style>
