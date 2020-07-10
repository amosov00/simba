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
      div(v-for="(address, i) in user.user_btc_addresses" :key="i").mb-2.addr
        div {{ address.address }}
        div(@click="removeAddress({address:address.address, type: 'btc'})").has-text-danger.addr__delete {{$t('wallet.delete_wallet')}}
    div.is-flex.align-items-center.mt-4
      div.mr-3
        img(:src="require('~/assets/images/eth.svg')" width="36")
      div
        div.is-flex.align-items-center
          div.is-size-5.has-text-weight-bold {{ $t('profile.eth_address_list') }}
          a(href="#" @click="addNewWalletModal('eth')").link.ml-2 {{$t('wallet.add_wallet')}}
        div.is-italic.has-text-grey-light {{ $t('profile.for_issue_simba') }}
    div.mt-3
      div(v-for="(address, i) in user.user_eth_addresses" :key="i").mb-2.addr
        div {{ address.address }}
        div(@click="removeAddress({address:address.address, type: 'eth'})").has-text-danger.addr__delete {{$t('wallet.delete_wallet')}}
</template>

<script>
import AddNewWallet from "~/components/AddNewWallet";

export default {
  name: "profile-bill",
  layout: "profile",

  components: { AddNewWallet },

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

    removeAddress(data) {
      if (data.type === "btc" && this.user.two_factor) {
        this.$buefy.dialog.prompt({
          type:'is-danger',
          inputAttrs: {
            placeholder: this.$i18n.t('wallet.pin_code'),
            value: "",
            maxlength: 6,
          },
          cancelText: this.$i18n.t('other.cancel'),
          confirmText: this.$i18n.t('other.delete'),
          trapFocus: true,
          onConfirm: async (value) => {
            await this.$store.dispatch("removeAddress", {...data, pin_code: value});
            this.$parent.$emit('close')
          }
        });
      } else {
        this.$buefy.dialog.confirm({
          title: this.$i18n.t('other.delete'),
          message: `${this.$i18n.t('wallet.delete_sure')}?`,
          cancelText: this.$i18n.t('other.cancel'),
          confirmText: this.$i18n.t('other.delete'),
          type: 'is-danger',
          onConfirm: async () => {
            await this.$store.dispatch("removeAddress", data);
            this.$parent.$emit('close')
          }
        })
      }
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
