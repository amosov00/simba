<template lang="pug">
  div
    div.is-flex.content-tabs
      n-link(to="/profile" exact-active-class="link--active").link.link--underlined.content-tabs-item Profile
    div.main-content
      div.has-text-weight-bold {{ user.first_name }} {{ user.last_name }}
      div.mt-2 Email: {{ user.email }}
      button.mt-2.btn(@click="logout") Log out
</template>

<script>
  export default {
    name: "profile",
    layout: "main",
    computed: {
      user() {
        return this.$store.getters.user;
      }
    },
    data: () => ({
    }),
    methods: {
      logout() {
        this.$authLogout();
      }
    },
  };
</script>

<style lang="sass" scoped>
</style>
