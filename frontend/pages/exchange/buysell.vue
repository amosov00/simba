<template lang="pug">
  div
    div.is-flex.content-tabs
      n-link(to="/exchange/buysell" active-class="link--active").link.link--underlined.content-tabs-item Buy/sell
      n-link(to="/exchange/bills" active-class="link--active").link.link--underlined.content-tabs-item Bills
    div.main-content
      div.position-relative
        n-link(to="/exchange/trade")
          img(src="~assets/images/back.svg").back-btn
      div.steps.is-flex.align-items-center
        div.operation.mr-4 {{ operation }}
        span(v-for="(step, i) in tradeData.steps.list" :key="i"
          @click="tradeData.steps.current = step" :class="{ 'steps-item--active': (i) < tradeData.steps.list.indexOf(tradeData.steps.current)+1}").steps-item {{ i+1 }}
      div.trade-content
        component(:is="tradeData.steps.current")
    b-modal(:active.sync="metamask_modal" has-modal-card :can-cancel="false")
     MetamaskWallet
</template>

<script>
  import WalletConfirm from "@/components/Trade/WalletConfirm"
  import CreatePayment from "@/components/Trade/CreatePayment"
  import BillPayment from "@/components/Trade/BillPayment"
  import Status from "@/components/Trade/Status"
  import Final from "@/components/Trade/Final"

  import Web3 from 'web3';
  import MetamaskWallet from "~/components/MetamaskWallet";

  export default {
    name: "exchange-buysell",
    layout: 'main',
    components: {MetamaskWallet, WalletConfirm, CreatePayment, BillPayment, Status, Final },
    async created() {
      await this.$store.dispatch('fetchContracts');
      console.log(this.$store.getters.contract);
    },
    computed: {
      metamask_modal() {
        return this.$store.getters['metamask/status'] !== 'online';
      }
    },
    data: () => {
      return {
        operation: 'Buy',
        tradeData: {
          steps: {
            current: 'WalletConfirm',
            list: ['WalletConfirm', 'CreatePayment', 'BillPayment', 'Status', 'Final']
          }
        },
        data: [
          { 'id': '#3', 'amount': '999 000 050 000', 'date': '01.06.2020', 'type': 'BUY', 'status': '1:15:47'},
          { 'id': '#2', 'amount': '999 000 050 000', 'date': '01.06.2020', 'type': 'Sell', 'status': 'Not paid' },
          { 'id': '#1', 'amount': '999 000 050 000', 'date': '01.06.2020', 'type': 'BUY', 'status': 'Paid' },
        ],
        columns: [
          { field: 'id', width: '40', }, { field: 'amount' }, { field: 'date', centered: true },
          { field: 'type' }, { field: 'status' }
        ]
      }
    }
  };
</script>

<style lang="sass" scoped>
  .trade-content
    margin-top: 50px
  .steps-item
    font-weight: 300
    font-size: 18px
    line-height: 100%
    text-align: center
    color: #FFFFFF
    background-color: #DFDFDF
    width: 30px
    height: 30px
    display: flex
    align-items: center
    justify-content: center
    border-radius: 100px
    margin-right: 70px
    position: relative
    &:not(:last-child)
      &::after
        content: ""
        width: 60px
        position: absolute
        border: 1px dashed #E5E5E5
        left: 35px
      top: 50%
    &:last-child
      margin-right: 0
    &--active
      background-color: #E0B72E

  .operation
    font-weight: bold
    font-size: 22px
    line-height: 144.19%
    color: #E0B72E
  .back-btn
    top: 5px
    position: absolute
    left: -70px
    &:hover
      cursor: pointer
      opacity: 0.7
</style>
