<template lang="pug">
  div.modal-card(style="max-width: 400px")
    header.modal-card-head
      p(class="modal-card-title") Add new {{ type.toUpperCase() }} wallet
    section.modal-card-body
      b-field
        b-input(v-model="wallet")
      button(@click="add" :disabled="!wallet").btn.w-100 Add
</template>

<script>

  import data from "~/pages/profile/data";

  export default {
    name: 'AddNewWallet',
    props: {
      type: String
    },
    data: () => ({
      wallet: ""
    }),
    methods: {
      async add(){
        let type_prop = 'user_btc_addresses';

        if(this.type === 'eth') {
          type_prop = 'user_eth_addresses';
        }

        if(this.$store.getters.user[type_prop].length) {
          let addr_list = JSON.parse(JSON.stringify(this.$store.getters.user[type_prop]));

          if(addr_list.indexOf(this.wallet) !== -1) {
            this.$buefy.toast.open({ message: "You already have this wallet in the list!", type: 'is-danger' })
            return
          }

          addr_list.push(this.wallet)

          let data_to_send = {[type_prop]: addr_list};

          if(await this.$store.dispatch('changeAddresses', data_to_send)) {
            this.$buefy.toast.open({ message: "Address successfully added!", type: 'is-primary' })
            this.$emit('close');
          } else {
            this.$buefy.toast.open({ message: "Something went wrong, your wallet address might be invalid!", type: 'is-danger' })
          }

          await this.$store.dispatch('getUser')
        }
      }
    }
  }
</script>

<style lang="sass" scoped>
</style>
