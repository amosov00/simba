<template lang="pug">
  div
    div.is-flex.content-tabs
      n-link(to="/profile" exact-active-class="link--active").link.link--underlined.content-tabs-item Profile
    div.main-content
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
            div.is-flex.space-between
              button.mt-4.btn(type="submit" :disabled="!changesFound || invalid") Save
              button.mt-4.btn(type="button" @click="logout") Log out
    b-modal(:active.sync="passChangeModal" has-modal-card)
      PasswordChange
    b-loading(is-full-page :active.sync="isLoading")
</template>

<script>
  import PasswordChange from "~/components/PasswordChange";

  export default {
    name: "profile",
    layout: "main",
    components: { PasswordChange },
    computed: {
      changesFound() {
        for(let prop in this.userData){
          if(this.userData[prop] !== this.orig_user[prop]){
            return true
          }
        }

        return false
      },
      btc_address() {
        return this.$store.getters.btc_address;
      }
    },
    data: () => ({
      isLoading: false,
      isSaveDisabled: true,
      orig_user: {},
      userData: {
        email: '',
        first_name: '',
        last_name: '',
      },
      passChangeModal: false
    }),
    methods: {
      async saveProfile() {
        this.isLoading = true;
        const resp = await this.$store.dispatch('changeProfile', this.userData);

        if(resp) {
          this.$buefy.toast.open({message: 'Succesfully changed!', type: 'is-primary'});
          if(!await this.$store.dispatch('getUser')) {
            window.location.reload(true)
          }
        } else {
          this.$buefy.toast.open({message: 'Error changing profile!', type: 'is-danger'});
        }
        this.isLoading = false;
      },
      logout() {
        this.$authLogout();
      }
    },
    mounted() {
      let { email, last_name, first_name } = this.$store.getters.user;

      this.userData.email = email;
      this.userData.first_name = first_name;
      this.userData.last_name = last_name;

      this.orig_user = this.userData;
    },
    async asyncData({ store }) {
      await store.dispatch('getBtcAddress')
    }
  };
</script>

<style lang="sass" scoped>
</style>
