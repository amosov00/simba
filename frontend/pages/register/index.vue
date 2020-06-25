<template lang="pug">
  div
    div.is-flex.content-tabs
      n-link(to="/" exact-active-class="link--active").link.link--underlined.content-tabs-item Sign in
      n-link(to="/register" exact-active-class="link--active").link.link--underlined.content-tabs-item Registration
    div.main-content
      div.column.is-4.p-0
        ValidationObserver(v-slot="{ handleSubmit }")
          form(@submit.prevent="handleSubmit(submit)")
            b-field
              ValidationProvider(rules="required|alpha_spaces|min:1" v-slot="{ errors }" name="first name")
                b-input(native-type="text" size="is-small" placeholder="first name" v-model="register_form.first_name")
                span.validaton-error {{ errors[0] }}
            b-field
              ValidationProvider(rules="required|alpha_spaces|min:1" v-slot="{ errors }" name="last name")
                b-input(native-type="text" size="is-small" placeholder="last name" v-model="register_form.last_name")
                span.validaton-error {{ errors[0] }}
            b-field
              //- ValidationProvider(rules="required|email" v-slot="{ errors }" name="email")
              b-input(native-type="text" size="is-small" placeholder="Referral id" v-model="register_form.referral_id")
                //- span.validaton-error {{ errors[0] }}
            b-field
              ValidationProvider(rules="required|email" v-slot="{ errors }" name="email")
                b-input(native-type="text" size="is-small" placeholder="email" v-model="register_form.email")
                span.validaton-error {{ errors[0] }}
            b-field
              ValidationProvider(rules="required|min:8|confirmed:confirmation" vid="confirmation" v-slot="{ errors }" name="password")
                b-input(type="password" size="is-small" placeholder="password" v-model="register_form.password")
                span.validaton-error {{ errors[0] }}
            b-field
              ValidationProvider(rules="required|min:8" v-slot="{ errors }" name="repeat password")
                b-input(type="password" size="is-small" placeholder="repeat password" v-model="register_form.repeat_password")
                span.validaton-error {{ errors[0] }}
            b-field
              ValidationProvider(:rules="{ required: { allowFalse: false } }" v-slot="{ errors }" name="accept conditions")
                b-checkbox(v-model="terms_and_conditions") I accept terms and conditions
                span.validaton-error {{ errors[0] }}
            b-button(native-type="submit").btn.w-100.mt-2 Sign up
    b-loading(is-full-page :active.sync="loading")
</template>

<script>
  import { ValidationProvider, ValidationObserver } from 'vee-validate';

  export default {
    name: "register",
    layout: "main",
    components: {
      ValidationProvider, ValidationObserver
    },
    data() {
      return {
        register_form: {
          first_name: "",
          last_name: "",
          email: "",
          repeat_password: "",
          password: "",
          referral_id: ""
        },
        terms_and_conditions: null,
        loading: false
      };
    },
    methods: {
      async submit() {
        this.loading = true;
        let resp = await this.$store.dispatch('signUp', this.register_form);

        if(!resp) {
          this.$buefy.toast.open({message: 'Error: failed to register', type: 'is-danger'})
        } else {
          this.$buefy.toast.open({message: 'Successfully registered! Please check your email to activate your account.', type: 'is-success', duration: '6000'})
          this.$nuxt.$router.replace({ path: '/'});
        }

        this.loading = false;
      }
    },
  };
</script>

<style lang="sass" scoped>

</style>
