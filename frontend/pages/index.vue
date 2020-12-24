<template lang="pug">
  div
    div.is-flex.content-tabs
      n-link(to="/" exact-active-class="link--active").link.link--underlined.content-tabs-item {{$t('auth.sign_in')}}
      n-link(to="/register" exact-active-class="link--active").link.link--underlined.content-tabs-item {{$t('auth.registration')}}
    div.main-content
      div.column.is-4.p-0
        b-field
          b-input(size="is-small" placeholder="e-mail" v-model="email")
        b-field
          b-input(size="is-small" type="password" :placeholder="$i18n.t('auth.password')" v-model="password" v-on:keypress.enter.native="login")
        b-button(:loading="loading" @click="login").btn.w-100 {{ $t('auth.sign_in') }}
        div.mt-2
          n-link(to="/forgot" exact-active-class="link--active").link.link--underlined {{ $t('auth.forgot_pw') }}

</template>

<script>
import Login2FA from "~/components/Login2FA";
export default {
  name: "index",
  layout: "main",
  components: { Login2FA },
  middleware({ store, redirect }) {
    if (store.state.user) {
      redirect("/profile/data/");
      return;
    }
  },
  data() {
    return {
      email: "",
      password: "",
      loading: false,
      modal2FA: true
    };
  },
  methods: {
    async login() {
      this.loading = true;
      this.$store.commit("setLoginDataBuffer", {
        email: this.email,
        password: this.password
      });
      let resp = await this.$authLogin(
        this.email,
        this.password
      );
      if(resp !== true) {
        if(resp.response.status >= 400) {
          let resp_msg = resp.response.data[0].message

          if (resp_msg === "Incorrect 2FA pin code") {
            this.$buefy.modal.open({
              parent: this,
              component: Login2FA,
              hasModalCard: true,
              customClass: "custom-class custom-class-2",
              trapFocus: true
            });
          } else {
            this.$buefy.toast.open({
              message:
                this.$i18n.t('auth.login_failed'),
              type: "is-danger",
              duration: 3500
            });
          }
        }
      }


      this.password = "";
      this.loading = false;
    }
  }
};
</script>

<style lang="sass" scoped></style>
