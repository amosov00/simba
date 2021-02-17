<template lang="pug">
  div.main-content
    h1.title.is-size-4 xPub
    div.mt-4.xpub.position-relative
      div.xpub__block(v-for="(item, i) in xpub" :key="i" @click="update(item)")
        img(:src="require(`@/assets/images/${flagImages[item.title.toLowerCase()]}`)").xpub__image
        div.xpub__title {{ item.title }}
        div.xpub__subtitle(v-if="item.xpub_preview") {{ item.xpub_preview }}
        div.xpub__status(:class="{'xpub__status--active': item.is_active}")
          |{{ item.is_active ? $i18n.t('xpub.status_active') : $i18n.t('xpub.status_inactive') }}
      b-loading(:active.sync="isLoading" :is-full-page="false")
</template>

<script>
export default {
  name: 'xpub',
  layout: 'main',
  middleware: ['adminRequired'],

  computed: {
    xpub() {
      return this.$store.getters['xpub/xpubList']
    },
  },

  data: () => ({
    isLoading: false,
    flagImages: {
      uae: 'uae.svg',
      liechtenstein: 'liechtenstein.png',
      newzealand: 'new-zeland.png',
      switzerland: 'switzerland.svg',
    },
  }),

  methods: {
    async update(xpub) {
      const data_to_send = {
        id: xpub._id,
        data: {
          is_active: !xpub.is_active,
        },
      }

      this.$buefy.dialog.confirm({
        title: this.$i18n.t('xpub.confirm_your_action'),
        message: this.$i18n.t('xpub.confirm_change_status'),
        cancelText: this.$i18n.t('other.cancel'),
        confirmText: this.$i18n.t('other.confirm'),
        type: xpub.is_active ? 'is-danger' : 'is-primary',
        onConfirm: async () => {
          this.isLoading = true
          if (await this.$store.dispatch('xpub/btcXpubUpdateSingle', data_to_send)) {
            this.$buefy.toast.open({ message: this.$i18n.t('xpub.status_changed'), type: 'is-primary' })
            await this.$store.dispatch('xpub/btcXpubFetchAll')
          } else {
            this.$buefy.toast.open({ message: this.$i18n.t('xpub.something_went_wrong'), type: 'is-danger' })
          }
          this.isLoading = false
        },
      })
    },
  },

  async asyncData({ store }) {
    await store.dispatch('xpub/btcXpubFetchAll')
  },
}
</script>

<style lang="sass">
.dialog .modal-card
  min-width: 400px

.xpub
  display: flex
  flex-wrap: wrap
  &__image
    margin-bottom: 10px
    max-height: 16px
  &__status
    margin-top: 5px
    &--active
      color: #0060FF
  &__block
    display: flex
    align-items: center
    flex-direction: column
    justify-content: center
    width: calc(25% - 15px)
    border: 1px solid #eeeeee
    min-height: 190px
    margin-right: 15px
    color: #333333
    &:hover
      cursor: pointer
      border: 1px solid #0060FF
    &:last-child
      margin-right: 0
  &__title
    font-size: 18px
    font-weight: 600
  &__subtitle
  font-size: 14px
  font-weight: 400
</style>
