<template lang="pug">
  div
    div.is-flex.content-tabs
      n-link(to="/" exact-active-class="link--active").link.link--underlined.content-tabs-item Sign in
      n-link(to="/register" exact-active-class="link--active").link.link--underlined.content-tabs-item Registration


</template>

<script>
  export default {
    name: "register",
    layout: "main",
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
