<template lang="pug">
  div
    div.is-flex.content-tabs
      n-link(to="/" exact-active-class="link--active").link.link--underlined.content-tabs-item Sign in
      n-link(to="/activate" active-class="link--active").link.link--underlined.content-tabs-item Activation
    div.main-content
      div.column.is-5.p-0
        b-field(label="Password")
          b-input(type="password" v-model="password")
        b-field(label="Repeat password")
          b-input(type="password" v-model="repeat_password")
        button.btn.w-100(@click="changePassword") Change password

</template>

<script>
  export default {
    name: "recover-index",
    layout: "main",
    data: () => ({
      password: '',
      repeat_password: '',
      query: {
        recover_code: ''
      },
    }),
    methods: {
      async changePassword(){
        this.loading = true;

        let data = { password: this.password, repeat_password: this.repeat_password, recover_code: this.query.recover_code}

        if(await this.$store.dispatch('finishRecover', data)) {
          this.$buefy.toast.open({message: 'Success!', type: 'is-primary'});
          this.$nuxt.$router.replace({ path: '/'});
        } else {
          this.$buefy.toast.open({message: 'Error', type: 'is-danger'});
        }

        this.email = ''

        this.loading = false;
      }
    },
    asyncData({ query }) {
      return { query }
    }
  };
</script>

<style lang="sass" scoped>
</style>
