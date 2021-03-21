<template lang="pug">
  div
    h3(v-if="isBuyInvoice").text-large.has-text-weight-bold {{ $t('exchange.confirm_wallet')}}

    div.is-flex.mt-2.align-items-center.space-between
      div(v-if="isBuyInvoice").is-flex.align-items-center
        img(:src="require('~/assets/images/eth.svg')").mr-2
        div.text-large {{ ethAddress }}

      div(v-else)
        div.is-size-6.mb-1
          span.has-text-weight-bold {{$t('exchange.choose_eth_wallet.p1')}}
          = ' '
          span.has-text-grey-light {{$t('exchange.choose_eth_wallet.p2')}}
        div.is-flex.align-items-center.mr-4
          b-select(expanded v-model="ethAddress").mr-3.wallet-select
            option(v-for="op in user.user_eth_addresses") {{ op.address }}
          a(href="#" @click="addNewWalletModal('eth')") {{$t('wallet.add_wallet')}}
        div.is-size-6.mt-4.mb-1
          span.has-text-weight-bold {{$t('exchange.choose_btc_wallet.p1')}}
          = ' '
          span.has-text-grey-light {{$t('exchange.choose_btc_wallet.p2')}}
        div.is-flex.align-items-center.mr-4
          b-select(expanded v-model="btcAddress").mr-3.wallet-select
            option(v-for="op in user.user_btc_addresses") {{ op.address }}
          a(href="#" @click="addNewWalletModal('btc')") {{$t('wallet.add_wallet')}}
        div.mt-4
          button.btn(@click="confirm") {{ $t('exchange.confirm')}}

      button.btn(@click="confirm" v-if="isBuyInvoice") {{ $t('exchange.confirm')}}

    div.mt-2.has-text-danger {{ errors[0] }}
</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from 'vuex'

import AddNewWallet from '~/components/AddNewWallet'
import {InvoiceTypeSlug, InvoiceTypeTextToEnum} from "~/consts";

// Step 1
export default {
  name: 'trade-choose-wallet',
  data: () => ({
    InvoiceTypeSlug,
    btcAddress: null,
    ethAddress: null,
    errors: [],
  }),

  components: {AddNewWallet},

  computed: {
    ...mapGetters("exchange", ["isBuyInvoice"]),
    ...mapState(["user", "metamaskEthAddress"]),
    ...mapState("exchange", ["operation"])
  },

  methods: {
    ...mapMutations({
      setMetamaskEthAddress: "setMetamaskEthAddress",
      setNextStep: "exchange/setNextStep",
      setAddresses: "exchange/setAddresses",
      setInvoiceId: "exchange/setInvoiceId",
    }),
    ...mapActions(["addAddress"]),
    ...mapActions("invoices", ["createInvoice", "updateInvoice"]),

    addNewWalletModal(type) {
      this.$buefy.modal.open({
        parent: this,
        component: AddNewWallet,
        trapFocus: true,
        props: {type},
      })
    },

    async proceedAddresses() {
      if (this.isBuyInvoice) {
        let userHasEthAddress = this.user.user_eth_addresses.find(
          (el) => el.address.toLocaleLowerCase() === this.metamaskEthAddress.toLocaleLowerCase()
        )
        if (!userHasEthAddress) {
          return await this.addAddress({
            type: 'eth',
            address: this.metamaskEthAddress,
            created_at: Date.now(),
          })
        }
      } else {
        if (!this.ethAddress) {
          this.errors.push(this.$i18n.t('exchange.choose_eth_wallet_error'))
          return
        }
        if (!this.btcAddress) {
          this.errors.push(this.$i18n.t('exchange.choose_btc_wallet_error'))
          return
        }
      }

      return true
    },

    async confirm() {
      const status = await this.proceedAddresses()

      if (!status) {
        return
      }
      let createdInvoice = await this.createInvoice({
        invoice_type: InvoiceTypeTextToEnum[this.operation]
      })

      if (!createdInvoice) {
        this.loading = false
        return
      }

      let updatedInvoice = await this.updateInvoice({
        id: createdInvoice._id,
        target_btc_address: this.btcAddress,
        target_eth_address: this.ethAddress,
        btc_amount: 0,
        simba_amount: 0,
      })

      if (!updatedInvoice) {
        this.loading = false
        return
      }

      this.setInvoiceId(createdInvoice._id)
      await this.setNextStep("ConfirmInvoice")
    },
  },

  async created() {
    if (window.ethereum !== undefined) {
      await window.ethereum
        .enable()
        .then((res) => {
          this.setMetamaskEthAddress(res[0])
          this.ethAddress = res[0]
          return true
        })
        .catch((_) => {
          this.$nuxt.$router.push({path: '/exchange/'})
          return false
        })
    } else {
      Toast.open({message: 'Metamask is not installed!', type: 'is-danger', duration: 4000})
      await this.$nuxt.$router.push({path: '/exchange/'})
    }
  }
}
</script>

<style lang="sass">
.wallet-select
  width: 500px

  .select
    select
      border: 1px solid rgba(0, 0, 0, 0)
      border-bottom: 1px solid #E5E5E5

      &:focus
        border: 1px solid #0060FF
        box-shadow: none

      &:hover
        border-bottom: 1px solid #0060FF
</style>
