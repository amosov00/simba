<template lang="pug">
  div
    div.main-content
      div.position-relative
        n-link(to="/exchange/")
          img(src="~assets/images/back.svg").back-btn
      div.steps.is-flex.align-items-center
        div.operation.mr-4 {{ operation }}
        span(v-for="(step, i) in tradeData.steps.list" :key="i" :class="{ 'steps-item--failed': failedStep(i), 'steps-item--active': activeStep(i)}").steps-item {{ i+1 }}
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

    methods: {
      activeStep(i) {
        if(this.failedStep(i)) {
          return false
        }

        return i < (this.tradeData.steps.list.indexOf(this.tradeData.steps.current)+1)
      },

      failedStep(i){
        if(this.stepFail) {
          if(i === this.stepFail) {
            return true
          }
        }

        return false
      }
    },

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

      this.$on('step_failed', () => {
        this.stepFail = this.tradeData.steps.list.indexOf(this.tradeData.steps.current)
      })


      if(this.$nuxt.$route.query['op']) {
        if(this.$nuxt.$route.query['op'] === 'buy') {
          this.operation = 'Buy';
          this.$store.commit('setTradeData', {prop: 'operation', value: 1})
        } else {
          this.operation = 'Sell'
          this.$store.commit('setTradeData', {prop: 'operation', value: 2})

          this.multi_props["op"] = 'sell'
        }
      }

      if(this.$nuxt.$route.query['id']) {
        let single_res = await this.$store.dispatch('invoices/fetchSingle', this.$nuxt.$route.query['id']);

        this.multi_props["no_create"] = true;
        this.multi_props["invoice"] = single_res._id;

        if(single_res) {
          if(single_res.status === 'waiting') {
            this.tradeData.steps.current = 'BillPayment'
          }
          else if(single_res.status === 'completed') {
            this.tradeData.steps.current = 'Final'
            this.multi_props["buy_info"] = {
              simba_issued: single_res.btc_txs[0].outputs[0].value,
              target_eth: single_res.target_eth_address,
              tx_hash: single_res.btc_txs[0].hash,
              btc_amount_proceeded: single_res.btc_amount_proceeded
            }
          }
        } else {
          this.$buefy.toast.open({message:'Error: invoice not found', type: 'is-danger'})
          this.$nuxt.context.redirect('/exchange/')
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
        stepFail: null,
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

  .operation
    font-weight: bold
    font-size: 22px
    line-height: 144.19%
    color: #E0B72E
</style>
