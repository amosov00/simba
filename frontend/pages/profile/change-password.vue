<template lang="pug">
  ValidationObserver(v-slot="{ handleSubmit }")
    form(@submit.prevent="handleSubmit(onSubmit)" style="max-width: 356px")
      div
        b-field
          ValidationProvider(rules="required" v-slot="{ errors }" :name="$i18n.t('password.current')")
            b-input(type="password" v-model="form.old_password" :placeholder="$i18n.t('password.current')" autocomplete="off").input--material
            span.validaton-error {{ errors[0] }}
        b-field
          ValidationProvider(rules="required|min:8|confirmed:confirmation" v-slot="{ errors }" :name="$i18n.t('password.new')")
            b-input(type="password" v-model="form.password" :placeholder="$i18n.t('password.new')" autocomplete="off").input--material
            span.validaton-error {{ errors[0] }}
        b-field
          ValidationProvider(rules="required" v-slot="{ errors }" vid="confirmation" :name="$i18n.t('password.confirm')")
            b-input(type="password" v-model="form.repeat_password" :placeholder="$i18n.t('password.confirm')" autocomplete="off").input--material
            span.validaton-error {{ errors[0] }}
        div.has-text-right
          b-button(type="is-primary" native-type="submit" :loading="isLoading" style="width: 50%") {{$t('other.change')}}
</template>

<script>
  import { ValidationProvider, ValidationObserver } from 'vee-validate';

  export default {
    name: 'profile-change-password',
    layout: "profile",
    components: { ValidationProvider, ValidationObserver },
    data: () => ({
      form: {
        old_password: '',
        password: '',
        repeat_password: '',
      },
      isLoading: false
    }),

    methods: {
      async onSubmit() {
        this.isLoading = true;
        const resp = await this.$store.dispatch('changePassword', this.form);

        if(resp) {
          this.$buefy.toast.open({message: this.$i18n.t('password.change_success'), type: 'is-primary'});
        } else {
          this.$buefy.toast.open({message: this.$i18n.t('password.change_error'), type: 'is-danger'});
        }
        this.isLoading = false;
      }
    }
  }
</script>

<style lang="sass" scoped>
</style>
