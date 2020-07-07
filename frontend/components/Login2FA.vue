<template lang="pug">
  div.card
    div.card-content
      h1.title.is-4 Enter your 2fa code
      b-field.mt-2
        b-input( type="number" placeholder="Pin code" v-model="pin_code")
      b-button(:loading="loading" :disabled="pin_code.toString().length != 6" @click="confirm").btn.w-100 Confirm
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
      if(!resp) {
        this.$buefy.toast.open({
          message:
            "Check your email/password and make sure you activated your account!",
          type: "is-danger",
          duration: 3500
        });
        this.$parent.close()
      } else {
        this.$parent.close()
      }
    }
  },
}
</script>

<style lang="scss">

</style>