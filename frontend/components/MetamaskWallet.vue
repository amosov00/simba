<template lang="pug">
  div.card.metamask-window
    div.card-content
      div.title.is-4 Add your address
      div
        img(:src="require('@/assets/images/metamask.svg')")
      div.mt-2
        div To add an address, connect your personal account to the Ethereum wallet. If this is your first time installing MetaMask.
        div.mt-2 For mobile devices we recommend the TrustWallet app.
      div.mt-4
        button.btn.w-100(:disabled="addDisabled" @click="connect") Connect Metamask
      div.mt-2(v-if="addDisabled").has-text-danger.has-text-centered Metamask extension is not installed
      div.has-text-centered.mt-4
        n-link(to="/exchange/trade/") Go back

</template>

<script>
  import Web3 from 'web3';

  export default {
    name: 'MetamaskWallet',
    data: () => ({
      addDisabled: false
    }),
    async created() {
      if (!window.ethereum) {
        this.addDisabled = true
      }
    },
    methods: {
      async connect() {
        let accounts = null;

        try{
          accounts = await window.ethereum.enable();
        } catch {
          return false
        }

        console.log(accounts);

        const account = accounts[0];
        window.web3 = new Web3(window.ethereum);
        window.web3.defaultAccount = account;


        console.log('Connected!')
        await this.$store.dispatch('metamask/set_address', account)
        await this.$store.dispatch('metamask/set_status', 'online')

        return true
      }
    }
  }
</script>

<style lang="sass" scoped>
  .metamask-window
    max-width: 647px
    padding: 20px 40px
</style>
