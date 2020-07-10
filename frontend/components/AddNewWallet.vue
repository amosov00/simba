<template lang="pug">
  div.modal-card(style="max-width: 500px")
    header.modal-card-head
      p(class="modal-card-title") {{$t('wallet.add_new_wallet.p1')}} {{ type.toUpperCase() }} {{$t('wallet.add_new_wallet.p2')}}
    section.modal-card-body
      b-field(:label="$i18n.t('other.address')")
        b-input(v-model="wallet")
      b-field(:label="$i18n.t('wallet.pin_code')" v-if="user.two_factor && type === 'btc'")
        b-input(type="number" v-model="pin_code")
      div.mt-3
        button(@click="add" v-if="type === 'btc'" :disabled="!wallet && pin_code.toString().length != 6").btn.w-100 {{$t('other.add')}}
        button(@click="add" v-else-if="type === 'eth'" :disabled="!wallet || metamask_window_opened").btn.w-100 {{$t('other.add')}}
</template>

<script>
export default {
  name: "AddNewWallet",
  props: {
    type: String
  },
  data: () => ({
    wallet: "",
    pin_code: "",
    metamask_window_opened: false,
  }),
  computed: {
    user() {
      return this.$store.getters.user;
    }
  },
  methods: {
    async add() {
      console.log(this.type)

      if(this.type === 'eth') {
        this.metamask_window_opened = true
      }

      this.$store.dispatch("addAddress", {
        type: this.type,
        address: this.wallet,
        created_at: Date.now(),
        pin_code: this.pin_code
      }).then(_ => {
        if(this.type === 'eth') {
          this.metamask_window_opened = false
        }
        this.$emit('close')
      }).catch(_ => {
        if(this.type === 'eth') {
          this.metamask_window_opened = false
          this.$buefy.toast.open({message: this.$i18n.t('wallet.failed_to_get_signature'), type: 'is-danger'})
        }
      })
    }
  }
};
</script>

<style lang="sass" scoped></style>
