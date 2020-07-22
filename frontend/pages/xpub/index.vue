<template lang="pug">
  div.main-content
    h1.title.is-size-4 xPub
    div.mt-4.xpub
      div.xpub__block(v-for="(item, i) in xpub" :key="i" @click="update(item)")
        div.xpub__title {{ item.title }}
        div.xpub__status(:class="{'xpub__status--active': item.is_active}") {{ item.is_active ? 'Active' : 'Not active' }}
</template>

<script>
  export default {
    name: "xpub",
    layout: "main",
    middleware: ["adminRequired"],


    computed: {
      xpub() {
        return this.$store.getters['xpub/xpubList']
      }
    },


    methods: {
      async update(xpub) {

        const data_to_send = {
          id: xpub._id,
          data: {
            is_active: !xpub.is_active
          }
        }

        if(await this.$store.dispatch('xpub/btcXpubUpdateSingle', data_to_send)) {
          this.$buefy.toast.open({message:'success', type:'is-primary'})
          await this.$store.dispatch("xpub/btcXpubFetchAll")
        } else {
          this.$buefy.toast.open({message:'error', type:'is-danger'})
        }
      }
    },

    async asyncData({store}) {
      await store.dispatch("xpub/btcXpubFetchAll")
    }
  };
</script>

<style lang="sass">
.xpub
  display: flex
  flex-wrap: wrap
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
</style>
