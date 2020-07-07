<template lang="pug">
  div
    div.is-flex.align-items-center
      div.mr-3
        img(:src="require('~/assets/images/bitcoin.svg')" width="36")
      div
        div.is-flex.align-items-center
          div.is-size-5.has-text-weight-bold {{ $t('profile.btc_address_list') }}
          a(href="#" @click="addNewWalletModal('btc')").link.ml-2 {{$t('wallet.add_wallet')}}
        div.is-italic.has-text-grey-light {{ $t('profile.for_withdraw_btc') }}
    div.mt-3
      div(v-for="(addr, i) in user.user_btc_addresses").mb-2.addr
        div {{ addr }}
        div(@click="removeAddress(i, 'user_btc_addresses')").has-text-danger.addr__delete {{$t('wallet.delete_wallet')}}
    div.is-flex.align-items-center.mt-4
      div.mr-3
        img(:src="require('~/assets/images/eth.svg')" width="36")
      div
        div.is-flex.align-items-center
          div.is-size-5.has-text-weight-bold {{ $t('profile.eth_address_list') }}
          a(href="#" @click="addNewWalletModal('eth')").link.ml-2 {{$t('wallet.add_wallet')}}
        div.is-italic.has-text-grey-light {{ $t('profile.for_issue_simba') }}
    div.mt-3
      div(v-for="(addr, i) in user.user_eth_addresses").mb-2.addr
        div {{ addr }}
        div(@click="removeAddress(i, 'user_eth_addresses')").has-text-danger.addr__delete {{$t('wallet.delete_wallet')}}
</template>

<script>
  import AddNewWallet from "~/components/AddNewWallet";

  export default {
    name: "profile-bill",
    layout: "profile",

    components: {AddNewWallet},

    data: () => ({
      eth_wallet_add_modal: false
    }),

    computed: {
      user() {
        return this.$store.getters.user;
      }
    },

    methods: {
      addNewWalletModal(type) {
        this.$buefy.modal.open({
          parent: this,
          component: AddNewWallet,
          hasModalCard: true,
          trapFocus: true,
          props: { type }
        });
      },

      removeAddress(index, type) {
        this.$buefy.dialog.confirm({
          title: this.$i18n.t('other.delete'),
          message: "<span class='is-size-6' style='line-height: 150%'>" + this.$i18n.t('wallet.delete_sure') + ": <strong>" + this.user[type][index] + "</strong><span>",
          confirmText: this.$i18n.t('other.delete'),
          cancelText: this.$i18n.t('other.cancel'),
          type: 'is-danger',
          onConfirm: async () => {
            let addr_list = JSON.parse(JSON.stringify(this.user[type]));
            addr_list.splice(index, 1)

            let data_to_send = {[type]: addr_list};

            if(await this.$store.dispatch('changeAddresses', data_to_send)) {
              this.$buefy.toast.open({ message: "Address successfully deleted!", type: 'is-primary' })
            } else {
              this.$buefy.toast.open({ message: "Error deleting address!", type: 'is-danger' })
            }

            await this.$store.dispatch('getUser')
          }
        })
      }
    }
  };
</script>

<style lang="sass" scoped>
  .addr
    display: flex
    align-items: center
    height: 21px
    &:hover
      color: #0060FF
      cursor: default
      .addr__delete
        display: inline-block
    &__delete
      display: none
      margin-left: 20px
      padding: 2px 20px
      background-color: transparent
      border-radius: 100px
      transition: background-color 300ms
      &:hover
        cursor: pointer
        background-color: #ffe8ef
      &:active
        opacity: 0.8
</style>
