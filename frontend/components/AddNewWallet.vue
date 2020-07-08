<template lang="pug">
  div.modal-card(style="max-width: 400px")
    header.modal-card-head
      p(class="modal-card-title") Add new {{ type.toUpperCase() }} wallet
    section.modal-card-body
      b-field(label="Wallet")
        b-input(v-model="wallet")
      b-field(label="2FA Code" v-if="user.two_factor && type === 'btc'")
        b-input(type="number" v-model="pin_code")
      button(@click="add" v-if="user.two_factor || type === 'btc'" :disabled="!wallet && pin_code.toString().length != 6").btn.w-100 Add
      button(@click.once="add" v-else-if="type === 'eth'" :disabled="!wallet").btn.w-100 Add
</template>

<script>
export default {
  name: "AddNewWallet",
  props: {
    type: String
  },
  data: () => ({
    wallet: "",
    pin_code: ""
  }),
  computed: {
    user() {
      return this.$store.getters.user;
    }
  },
  methods: {
    async add() {
      await this.$store.dispatch("addAddress", {
        type: this.type,
        address: this.wallet,
        created_at: Date.now(),
        pin_code: this.pin_code
      });
      await this.$store.dispatch("getUser");
    }
  }
};
</script>

<style lang="sass" scoped></style>
