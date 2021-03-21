<template lang="pug">
  div
    div.is-flex.content-tabs
      n-link(to="/" exact-active-class="link--active").link.link--underlined.content-tabs-item {{$t('auth.sign_in')}}
      n-link(to="/register" exact-active-class="link--active").link.link--underlined.content-tabs-item {{$t('auth.registration')}}
    div.main-content
      div.column.is-6.p-0
        ValidationObserver(v-slot="{ handleSubmit }")
          form(@submit.prevent="handleSubmit(submit)")
            div.form-row
              b-field.form-row__item
                ValidationProvider(ref="email" rules="required|email" v-slot="{ errors }" name="email")
                  b-input(native-type="text" size="is-small" placeholder="email" v-model="register_form.email")
                  span.validaton-error {{ errors[0] }}
              b-field.form-row__item
                b-input(native-type="text" size="is-small" placeholder="@telegram" v-model="register_form.telegram")
            div.form-row
              b-field.form-row__item
                ValidationProvider(ref="first_name" rules="required|alpha_spaces|min:1" v-slot="{ errors }" :name="$i18n.t('auth.first_name').toLocaleLowerCase()")
                  b-input(native-type="text" size="is-small" :placeholder="$i18n.t('auth.first_name').toLocaleLowerCase()" v-model="register_form.first_name")
                  span.validaton-error {{ errors[0] }}
              b-field.form-row__item
                ValidationProvider(ref="last_name" rules="required|alpha_spaces|min:1" v-slot="{ errors }" :name="$i18n.t('auth.last_name').toLocaleLowerCase()")
                  b-input(native-type="text" size="is-small" :placeholder="$i18n.t('auth.last_name').toLocaleLowerCase()" v-model="register_form.last_name")
                  span.validaton-error {{ errors[0] }}
            div.form-row
              b-field.form-row__item
                ValidationProvider(ref="password" rules="required|min:8|confirmed:repeat_password" vid="confirmation" v-slot="{ errors,validate }" :name="$i18n.t('auth.password').toLocaleLowerCase()")
                  b-input(type="password" size="is-small" :placeholder="$i18n.t('auth.password').toLocaleLowerCase()" v-model="register_form.password")
                  span.validaton-error {{ errors[0] }}
              b-field.form-row__item
                ValidationProvider(ref="repeat_password" rules="required|min:8" vid="repeat_password" v-slot="{ errors }" :name="$i18n.t('auth.repeat_password').toLocaleLowerCase()")
                  b-input(type="password" size="is-small" :placeholder="$i18n.t('auth.repeat_password').toLocaleLowerCase()" v-model="register_form.repeat_password")
                  span.validaton-error {{ errors[0] }}
            b-field
              ValidationProvider(ref="referral_id" rules="required" v-slot="{ errors }" :name="$i18n.t('auth.partner_id').toLocaleLowerCase()")
                b-input(native-type="text" size="is-small" :placeholder="$i18n.t('auth.partner_id').toLocaleLowerCase()" v-model="register_form.referral_id")
                span.validaton-error {{ errors[0] }}
            b-field.terms
              ValidationProvider(ref="terms_of_agreement" :rules="{ required: { allowFalse: false } }" v-slot="{ errors }" :name="$i18n.t('auth.terms_of_agreement')" tag="div")
                b-checkbox(v-model="terms_and_conditions")
                  span {{$t('auth.i_accept')}}
                  =' '
                  a(href="https://simba.storage/terms-of-use.pdf" target="_blank" rel="noreferrer noopener").link {{$i18n.t('auth.terms_of_agreement')}}
                span.validaton-error {{ errors[0] }}
            b-button(native-type="submit").btn.mt-2 {{$i18n.t('auth.sign_up')}}
    b-loading(is-full-page :active.sync="loading")
</template>

<script>
import { ValidationObserver, ValidationProvider } from 'vee-validate'

export default {
  name: 'register',
  layout: 'main',
  middleware({ store, redirect }) {
    if (store.state.user) {
      redirect('/exchange/')
    }
  },
  components: {
    ValidationProvider,
    ValidationObserver,
  },
  data() {
    return {
      register_form: {
        first_name: '',
        last_name: '',
        email: '',
        repeat_password: '',
        password: '',
        referral_id: 123,
        telegram: '',
      },
      terms_and_conditions: null,
      loading: false,
    }
  },
  created() {
    if (this.$route.query.referral_id) {
      this.$cookies.set('referral_id', this.$route.query.referral_id)
    }
    this.register_form.referral_id = this.$route.query.referral_id || this.$cookies.get('referral_id')
  },
  watch: {
    '$i18n.locale': function () {
      console.log(this.$refs.first_name.errors.length)
      setTimeout(() => {
        if (this.$refs.first_name.errors.length !== 0) {
          this.$refs.first_name.validate()
        }
        if (this.$refs.last_name.errors.length !== 0) {
          this.$refs.last_name.validate()
        }
        if (this.$refs.email.errors.length !== 0) {
          this.$refs.email.validate()
        }
        if (this.$refs.repeat_password.errors.length !== 0) {
          this.$refs.repeat_password.validate()
        }
        if (this.$refs.password.errors.length !== 0) {
          this.$refs.password.validate()
        }
        if (this.$refs.referral_id.errors.length !== 0) {
          this.$refs.referral_id.validate()
        }
        if (this.$refs.terms_of_agreement.errors.length !== 0) {
          this.$refs.terms_of_agreement.validate()
        }
      })
    },
  },
  methods: {
    async submit() {
      this.loading = true
      let resp = await this.$store.dispatch('signUp', this.register_form)
      if (resp) {
        await this.$router.replace({ path: '/' })
      }
      this.loading = false
    },
  },
}
</script>

<style lang="sass" scoped>
.field
  margin-bottom: 0
.field:not(:last-child)
  margin-bottom: 0
.terms
  padding-left: 20px
  padding-top: 20px
.form-row
  display: flex
  margin-bottom: 5px
  &:last-child
    margin-bottom: 0
  &__item
    width: 50%
    padding-left: 5px
    padding-right: 5px
    &:first-child
      padding-left: 0
    &:last-child
      padding-right: 0
</style>
