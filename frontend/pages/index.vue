<template lang="pug">
  div
    div.is-flex.content-tabs
      n-link(to="/" exact-active-class="link--active").link.link--underlined.content-tabs-item Sign in
      n-link(to="/register" exact-active-class="link--active").link.link--underlined.content-tabs-item Registration
    div.main-content
      div.column.is-4.p-0
        b-field
          b-input(size="is-small" placeholder="e-mail" v-model="email")
        b-field
          b-input(size="is-small" type="password" placeholder="password" v-model="password" v-on:keypress.enter.native="login")
        b-field
          b-input(size="is-small" type="number" placeholder="pin code" v-model="pin_code")
        b-button(:loading="loading" @click="login").btn.w-100 Sign in
        div.mt-2
          n-link(to="/forgot" exact-active-class="link--active").link.link--underlined Forgot password?

</template>

<script>
export default {
  name: "index",
  layout: "main",
  middleware ({ store, redirect }) {
    if(store.state.user) {
      redirect('/profile/data/')
      return
    }
  },
  data() {
    return {
      email: "",
      password: "",
      pin_code: null,
      loading: false
    };
  },
  methods: {
    async login() {
      this.loading = true;
      let resp = await this.$authLogin(this.email, this.password, this.pin_code);

      if(!resp) {
        this.$buefy.toast.open({message: 'Check your email/password and make sure you activated your account!', type: 'is-danger', duration: 3500})
      } else if (resp.response.data[0].message === 'Incorrect 2FA pin code') {
        console.log('show modal')
      }

      this.password = "";
      this.loading = false;
    }
  },
  async mounted() {
  }
};
</script>

<style lang="sass" scoped>
</style>
