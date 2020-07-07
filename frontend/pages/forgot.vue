<template lang="pug">
  div
    div.is-flex.content-tabs
      n-link(to="/forgot" exact-active-class="link--active").link.link--underlined.content-tabs-item {{$t('auth.sign_in')}}
      n-link(to="/register" exact-active-class="link--active").link.link--underlined.content-tabs-item {{$t('auth.registration')}}
    div.main-content
      div.position-relative
        n-link(to="/")
          img(src="~assets/images/back.svg").back-btn
      div.column.is-4.p-0
        b-field
          b-input(size="is-small" placeholder="e-mail" v-model="email")
        b-button(:loading="loading" @click="recover").btn.w-100 {{$t('auth.submit')}}

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
          this.$buefy.toast.open({message: this.$i18n.t('auth.recover_success'), type: 'is-primary'});
          this.email = ''
          this.$nuxt.$router.replace({ path: '/'});
        } else {
          this.$buefy.toast.open({message: this.$i18n.t('auth.recover_error'), type: 'is-danger'});
        }

        this.loading = false;
      }
    },
  };
</script>

<style lang="sass" scoped>
</style>
