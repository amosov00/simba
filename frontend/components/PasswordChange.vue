<template lang="pug">
  ValidationObserver(v-slot="{ handleSubmit }")
    form(@submit.prevent="handleSubmit(onSubmit)")
      div.modal-card(style="max-width: 300px")
        header.modal-card-head
          p(class="modal-card-title") Password change
        section.modal-card-body
          b-field
            ValidationProvider(rules="required" v-slot="{ errors }" name="Current password")
              b-input(type="password" v-model="form.old_password" placeholder="Current password")
              span.validaton-error {{ errors[0] }}
          b-field
            ValidationProvider(rules="required|min:8|confirmed:confirmation" v-slot="{ errors }" name="New password")
              b-input(type="password" v-model="form.password" placeholder="New password")
              span.validaton-error {{ errors[0] }}
          b-field
            ValidationProvider(rules="required" v-slot="{ errors }" vid="confirmation" name="Password confirmation")
              b-input(type="password" v-model="form.repeat_password" placeholder="Password confirmation")
              span.validaton-error {{ errors[0] }}
        footer.modal-card-foot
          b-button(type="is-primary" native-type="submit" :loading="isLoading") Change password
</template>

<script>
import { ValidationProvider, ValidationObserver } from 'vee-validate'

export default {
  name: 'PasswordChange',
  components: { ValidationProvider, ValidationObserver },
  data: () => ({
    form: {
      old_password: '',
      password: '',
      repeat_password: '',
    },
    isLoading: false,
  }),

  methods: {
    async onSubmit() {
      this.isLoading = true
      const resp = await this.$store.dispatch('changePassword', this.form)

      if (resp) {
        this.$parent.close()
        this.$buefy.toast.open({ message: 'Succesfully changed!', type: 'is-primary' })
      } else {
        this.$buefy.toast.open({ message: 'Error changing password!', type: 'is-danger' })
      }
      this.isLoading = false
    },
  },
}
</script>

<style lang="sass" scoped></style>
