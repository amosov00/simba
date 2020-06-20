<template lang="pug">
  div
    div.is-flex.content-tabs
      n-link(to="/forgot" exact-active-class="link--active").link.link--underlined.content-tabs-item Sign in
      n-link(to="/register" exact-active-class="link--active").link.link--underlined.content-tabs-item Registration
    div.main-content
      div.position-relative
        n-link(to="/")
          img(src="~assets/images/back.svg").back-btn
      div.column.is-4.p-0
        b-field
          b-input(size="is-small" placeholder="e-mail" v-model="email")
        b-button(:loading="loading" @click="recover").btn.w-100 Submit

</template>

<script>
  export default {
    name: "forgot",
    layout: "main",
    data() {
      return {
        email: '',
        loading: false
      };
    },
    methods: {
      async recover(){
        this.loading = true;

        if(await this.$store.dispatch('startRecover', {"email": this.email})) {
          this.$buefy.toast.open({message: 'Success! Please check your email for further instructions.', type: 'is-primary'});
          this.$nuxt.$router.replace({ path: '/'});
        } else {
          this.$buefy.toast.open({message: 'Error', type: 'is-danger'});
        }

        this.email = ''

        this.loading = false;
      }
    },
  };
</script>

<style lang="sass" scoped>
</style>
