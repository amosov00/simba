<template lang="pug">
  div
    div.is-flex.content-tabs
      n-link(to="/" exact-active-class="link--active").link.link--underlined.content-tabs-item Sign in
      n-link(to="/activate" active-class="link--active").link.link--underlined.content-tabs-item Activation
    div.main-content
      div.column.is-5.p-0
        b-field(label="Email")
          b-input(v-model="query.email")
        b-field(label="Verification code")
          b-input(v-model="query.verification_code")
        button.btn.w-100(@click="activate") Activate

</template>

<script>
  export default {
    name: "activate-index",
    layout: "main",
    data: () => ({
      query: {
        verification_code: '',
        email: ''
      },
    }),
    methods: {
      async activate(){
        if(!await this.$store.dispatch('activateAccount', this.query)) {
          this.$buefy.toast.open({message: 'Error: invalid email/code or account is already activated', type: 'is-danger'})
        } else {
          this.$buefy.toast.open({message: 'You successfully verifed your account!', type: 'is-success'})
          this.$nuxt.$router.replace({ path: '/'});
        }
      }
    },
    asyncData({ query }) {
      return { query }
    }
  };
</script>

<style lang="sass" scoped>
</style>
