<template lang="pug">
  div
    div.is-flex.content-tabs
      n-link(to="/" exact-active-class="link--active").link.link--underlined.content-tabs-item Sign in
      n-link(to="/register" exact-active-class="link--active").link.link--underlined.content-tabs-item Registration
    div.main-content
      div.column.is-4
        b-field
          b-input(size="is-small" placeholder="e-mail" v-model="email")
        b-field
          b-input(size="is-small" type="password" placeholder="password" v-model="password" v-on:keypress.enter.native="login")
        b-button(:loading="loading" @click="login").btn.w-100 Войти

</template>

<script>
export default {
  name: "index",
  layout: 'main',
  component: {

  },
  data() {
    return {
      email: "",
      password: "",
      loading: false
    };
  },
  methods: {
    async login() {
      this.loading = true;
      let resp = await this.$authLogin(this.email, this.password);
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
