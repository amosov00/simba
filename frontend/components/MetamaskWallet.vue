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

        await this.$store.dispatch('fetchContracts');
        console.log(this.$store.getters.contract);

        let miniToken = new web3.eth.Contract(this.$store.getters.contract.abi, this.$store.getters.contract.address)

        console.log(miniToken)

        console.log('Account balance:', await web3.eth.getBalance(account));

        await miniToken.methods.name().call().then(res => console.log(res));
        await miniToken.methods.totalSupply().call().then(res => console.log(res));


        miniToken.methods.balanceOf(account)
          .call()
          .then(balance => {
            console.log(balance / 1e18)
            return true;
          })
          .catch(() => {
            return false;
          });

        miniToken.methods.transfer(account, 0).call().then(res => {
          console.log(res)
        })

        miniToken.methods.approve(account, 1).call().then(res => {
          console.log(res)
        })

        /*const transactionParameters = {
          nonce: '0x00', // ignored by MetaMask
          gasPrice: '0x09184e72a000', // customizable by user during MetaMask confirmation.
          gas: '0x2710', // customizable by user during MetaMask confirmation.
          to: '0x0000000000000000000000000000000000000000', // Required except during contract publications.
          from: ethereum.selectedAddress, // must match user's active address.
          value: '0x00', // Only required to send ether to the recipient from the initiating external account.
          data:
            '0x7f7465737432000000000000000000000000000000000000000000000000000000600057', // Optional, but used for defining smart contract creation and interaction.
          chainId: 3, // Used to prevent transaction reuse across blockchains. Auto-filled by MetaMask.
        };

        window.web3.eth.sendTransaction({
          method: 'eth_sendTransaction',
          params: [transactionParameters],
          from: ethereum.selectedAddress,
        }, (res) => {
          console.log(res);
        })*/


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
