<template lang="pug">
  div
    div.is-flex.content-tabs
      n-link(to="/recover" active-class="link--active").link.link--underlined.content-tabs-item {{$t('auth.forgot_pw')}}
    div.main-content
      div.column.is-4.p-0
        b-field(:label="$i18n.t('password.new')")
          b-input(size="is-small" type="password" v-model="password")
        b-field(:label="$i18n.t('password.confirm')")
          b-input(size="is-small" type="password" v-model="repeat_password")
        button.btn.w-100(@click="changePassword") {{$t('auth.submit')}}

</template>

<script>
export default {
  name: 'recover-index',
  layout: 'main',
  data: () => ({
    password: '',
    repeat_password: '',
    query: {
      recover_code: '',
    },
  }),
  methods: {
    async changePassword() {
      this.loading = true

      let data = {
        password: this.password,
        repeat_password: this.repeat_password,
        recover_code: this.query.recover_code,
      }

      if (await this.$store.dispatch('finishRecover', data)) {
        this.$buefy.toast.open({ message: this.$i18n.t('password.change_success'), type: 'is-primary' })
        this.$nuxt.context.redirect('/')
      } else {
        this.$buefy.toast.open({ message: this.$i18n.t('password.change_error'), type: 'is-danger' })
      }

      this.loading = false
    },
  },
  asyncData({ query }) {
    return { query }
  },
}
</script>

<style lang="sass" scoped></style>
