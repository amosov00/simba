<template lang="pug">
  div.card.metamask-window
    div.card-content
      div.title.is-4 Add new ETH address
      div
        img(:src="require('@/assets/images/metamask.svg')")
      div.mt-2
        div To add a new address, connect your personal account to the Ethereum wallet. If this is your first time, please install MetaMask extension.
        div.mt-2 For mobile devices we recommend the TrustWallet app.
      div.mt-4
        button.btn.w-100(@click="addAddress") Add
</template>

<script>
import web3 from "~/plugins/web3";
export default {
  name: "MetamaskWallet",
  data: () => ({
    addressSelected: false
  }),
  methods: {
    addAddress() {
      console.log(web3);
      var msg =
        "0x879a053d4800c6354e76c7985a865d2922c82fb5b3f4577b2fe08b998954f2e0";
      var from = window.ethereum.selectedAddress;
      if (!from) return connect();
      web3.eth.sign(from, msg, function(err, result) {
        if (err) return console.error(err);
        console.log("SIGNED:" + result);
      });

      // this.$store.dispatch(
      //   "metamask/signAddress",
      //   window.ethereum.selectedAddress
      // );
    }
  }
};
</script>

<style lang="sass" scoped>
.metamask-window
  max-width: 647px
  padding: 20px 40px
</style>
