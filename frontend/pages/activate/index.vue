<template lang="pug">
  div
    div.is-flex.content-tabs
      n-link(to="/activate" active-class="link--active").link.link--underlined.content-tabs-item {{$t('auth.activation')}}
    div.main-content
      b-message(type="is-danger" v-if="success === false") {{ error_message }}

</template>

<script>
export default {
  name: 'activate-index',
  layout: 'main',
  data: () => ({
    query: {
      verification_code: '',
      email: '',
    },
    error_message: '',
  }),
  methods: {},
  async mounted() {
    if (this.success) {
      this.$buefy.toast.open({ message: this.$i18n.t('auth.activation_success'), type: 'is-primary' })
      this.$nuxt.context.redirect('/')
    } else {
      this.error_message = this.$i18n.t('auth.activation_failed')
    }
  },
  async asyncData({ query, store }) {
    let res = await store.dispatch('activateAccount', query)

    if (res) {
      return { success: true, res }
    } else {
      return { success: false }
    }
  },
}
</script>

<style lang="sass" scoped></style>
