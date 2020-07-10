<template lang="pug">
  div.card
    div.card-content
      h1.title.is-4 {{$t('auth.pin_code')}}
      b-field.mt-2
        b-input(v-model="pin_code" maxlength="6")
      b-button(:loading="loading" :disabled="pin_code.toString().length != 6" @click="confirm").btn.w-100 {{$t('auth.submit')}}
</template>

<script>
export default {
  data() {
    return {
      loading: false,
      pin_code: ''
    }
  },
  computed: {
    loginData() {
      return this.$store.getters.loginDataBuffer
    }
  },
  methods: {
    async confirm() {
      let resp = await this.$authLogin(this.loginData.email, this.loginData.password, this.pin_code);

      if(resp !== true) {
        if(resp.response.status >= 400) {
          this.$buefy.toast.open({
            message:
              this.$i18n.t('auth.login_failed_pin'),
            type: "is-danger",
            duration: 3500
          });
          this.pin_code = ''

          return
        }
      }

      this.$parent.close()
    }
  },
}
</script>

<style lang="scss">

</style>
