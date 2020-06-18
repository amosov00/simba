<template lang="pug">
  div
    div.main-content
      div wallet
      button(@click="launch") Metamask
    b-modal(:active.sync="showModalNew" has-modal-card :can-cancel="false")
      MetamaskWallet
</template>

<script>
  import MetamaskWallet from "~/components/MetamaskWallet";

  export default {
    name: "wallet-index",
    components: {MetamaskWallet},
    layout: "main",
    data() {
      return {
        showModalNew: false
      };
    },
    methods: {
      launch() {
        //this.showModalNew = true
        this.$buefy.modal.open({
          parent: this,
          component: MetamaskWallet,
          hasModalCard: true,
          'can-cancel': false
        })
      }
    },
  };
</script>

<style lang="sass" scoped>
</style>
