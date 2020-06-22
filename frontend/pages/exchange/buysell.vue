<template lang="pug">
  div
    div.main-content
      div.position-relative
        n-link(to="/exchange/")
          img(src="~assets/images/back.svg").back-btn
      div.steps.is-flex.align-items-center
        div.operation.mr-4 {{ operation }}
        span(v-for="(step, i) in tradeData.steps.list" :key="i" :class="{ 'steps-item--active': (i) < tradeData.steps.list.indexOf(tradeData.steps.current)+1}").steps-item {{ i+1 }}
      div.trade-content
        component(:is="tradeData.steps.current" :multi_props="multi_props")
</template>

<script>
  import WalletConfirm from "@/components/Trade/WalletConfirm"
  import CreatePayment from "@/components/Trade/CreatePayment"
  import BillPayment from "@/components/Trade/BillPayment"
  import Status from "@/components/Trade/Status"
  import Final from "@/components/Trade/Final"

  export default {
    name: "exchange-buysell",
    layout: 'main',
    components: { WalletConfirm, CreatePayment, BillPayment, Status, Final },

    async middleware ({ redirect, store }) {
      if (window.ethereum !== undefined) {
        await window.ethereum.enable().then(res => {
          store.commit('exchange/setTradeData', { prop: 'eth_address', value: res[0]})
          return true
        }).catch(_ => {
          redirect('/exchange/')
          return false
        })
      } else {
        console.log('metamask not found')

        redirect('/exchange/')
      }
    },

    async beforeMount() {
      this.$on('nextStep', () => {
        let steps = this.tradeData.steps;
        steps.current = steps.list[steps.list.indexOf(steps.current)+1]
      });


      if(this.$nuxt.$route.query['op']) {
        if(this.$nuxt.$route.query['op'] === 'buy') {
          this.operation = 'Buy';
          this.$store.commit('setTradeData', {prop: 'operation', value: 1})
        } else {
          this.operation = 'Sell'
          this.$store.commit('setTradeData', {prop: 'operation', value: 2})
        }
      }

      if(this.$nuxt.$route.query['id']) {
        let single_res = await this.$store.dispatch('invoices/fetchSingle', this.$nuxt.$route.query['id']);

        if(single_res) {
          if(single_res.status === 'waiting') {
            this.tradeData.steps.current = 'BillPayment'
          }
          else if(single_res.status === 'completed') {
            this.tradeData.steps.current = 'Status'
          }
        } else {
          this.$buefy.toast.open({message:'Error: invoice not found', type: 'is-danger'})
          this.$nuxt.context.redirect('/exchange/')
        }

        this.multi_props = {
          no_create: true,
          invoice: single_res._id
        }
      }

/*      if(this.$nuxt.$route.query['op'])*/

/*      let web3_metamask = new Web3(window.ethereum);

      this.tradeData.ethAddress = await web3_metamask.eth.getAccounts().then(res => res[0]);*/

/*      setTimeout(_ => {
        this.tradeData.ethAddress = web3_metamask.selectedAddress;
        console.log(window.ethereum.selectedAddress)
      }, 300)*/
    },

    data: () => {
      return {
        multi_props: {},
        operation: 'Buy',
        tradeData: {
          ethAddress: '',
          steps: {
            current: 'WalletConfirm',
            list: ['WalletConfirm', 'CreatePayment', 'BillPayment', 'Status', 'Final']
          }
        },
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
</style>
