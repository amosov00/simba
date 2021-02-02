<template lang="pug">
  div.main-content
    div.is-size-4.mb-3
      strong {{$t('su_invoices.invoice')}}
      =' — '
      span {{invoice._id}}
    div(v-for="(el, key) in invoice").is-flex.invoice-field
      div.invoice-field__label {{ $t(`su_invoices.${key}`) }}:
      div.flex-1
        div(v-if="Array.isArray(el)")
          div(v-if="el.length > 0")
            div(v-for="(item, i) in el" :key="i")
              div(v-if="typeof item === 'object'") -
                //--div(v-for="(value, key) in item") {{key}}: {{value}}
              div(v-else)
                a(:href="getBlockchainLink(item, 'tx', 'eth')" target="_blank" rel="noreferrer noopener" v-if="key === 'sst_tx_hashes'") {{ item }}
                a(:href="getBlockchainLink(item, 'tx', 'eth')" target="_blank" rel="noreferrer noopener" v-if="key === 'eth_tx_hashes'") {{ item }}
                a(:href="getBlockchainLink(item, 'tx', 'btc')" target="_blank" rel="noreferrer noopener" v-if="key === 'btc_tx_hashes'") {{ item }}
          div(v-else) {{ $t(`su_invoices.empty`) }}
        div(v-else)
          div(v-if="el === null") {{ $t(`su_invoices.not_available`) }}
          div(v-else)
            div(v-if="key === 'invoice_type'") {{ el === 1 ? $i18n.t('exchange.buy') : $i18n.t('exchange.sell') }}
            div(v-else-if="key === 'status'") {{ $t(`exchange.statuses.${el}`)}}
            div(v-else-if="key === 'created_at' || key === 'finised_at'") {{ timestampFromUtc(el) }}
            div(v-else-if="key === 'simba_amount_proceeded' || key === 'simba_amount'") {{ simbaFormat(el) }}
            div(v-else-if="key === 'btc_amount_proceeded' || key === 'btc_amount'") {{ btcFormat(el) }}
            a(v-else-if="key === 'target_eth_address'" :href="getBlockchainLink(el, 'address', 'eth')" target="_blank" rel="noreferrer noopener") {{ el }}
            a(v-else-if="key === 'target_btc_address'" :href="getBlockchainLink(el, 'address', 'btc')" target="_blank" rel="noreferrer noopener") {{ el }}
            n-link(v-else-if="key === 'user_id'" :to="`/admin/users/${el}`") {{ el }}
            div(v-else) {{ el }}
    div.is-flex.invoice-field
      div.invoice-field__label {{ $t(`su_invoices.sst_tx_detailed`) }}:
      div.flex-1
        div(@click="loadSstTransactions" v-if="!sstTableShow").link {{ $t(`su_invoices.sst_tx_table.show`) }}
        div(v-else @click="sstTableShow = false").link {{ $t(`su_invoices.sst_tx_table.hide`) }}
        div(v-if="sstTableShow && sstTransactions.length === 0").mt-2 {{ $t(`su_invoices.empty`) }}
        div(v-if="sstTableShow && sstTransactions.length > 0").mt-2
          b-table(:data="sstTransactions" hoverable)
            template(slot-scope="props")
              b-table-column(field="user_id" label="ID" sortable)
                n-link(:to="`/admin/users/${props.row.user_id}`") {{ props.row.user_id }}
              b-table-column(field="transactionHash" label="Tx Hash" sortable)
                b-tooltip(:label="props.row.transactionHash")
                    a(:href="getBlockchainLink(props.row.transactionHash, 'tx', 'eth')" target="blank" rel="noopener noreferrer") {{ truncateHash(props.row.transactionHash) }}
              b-table-column(field="level" label="Level" sortable) {{ props.row.level }}
              b-table-column(field="amount" label="Amount" sortable) {{ sstFormat(props.row.amount) }}

</template>

<script>
import formatDate from "~/mixins/formatDate";
import formatCurrency from "~/mixins/formatCurrency";

import invoiceMixins from "~/mixins/invoiceMixins";

export default {
  name: "invoicesById",
  layout: "main",
  middleware: ["adminRequired"],
  mixins: [formatDate, formatCurrency, invoiceMixins],

  data: () => ({
    sstTransactions: [],
    sstTableShow: false
  }),

  methods: {
    async loadSstTransactions() {
      this.sstTransactions = await this.$store.dispatch('meta/fetchInvoiceSstTransactions', this.invoice._id)

/*      this.sstTransactions = [
        {
          "transactionHash": "444444444444",
          "amount": 50,
          "user_id": "2d3123r12w31",
          "level": 1
        },
        {
          "transactionHash": "444444444444",
          "amount": 50,
          "user_id": "2d3123r12w31",
          "level": 1
        }
      ]*/

      this.sstTableShow = true
    }
  },

  async asyncData({store, route}) {
    const invoice = await store.dispatch('invoices/fetchAdminSingleInvoice', route.params.id)

    if('btc_txs' && 'eth_txs' in invoice) {
      delete invoice['btc_txs']
      delete invoice['eth_txs']
    }

    return {
      invoice
    }
  }
};
</script>

<style lang="sass" scoped>
.sst-table
  border-top: 1px solid #eeeeee
  border-left: 1px solid #eeeeee
.sst-table-cell
  border-bottom: 1px solid #eeeeee
  border-right: 1px solid #eeeeee
  padding: 8px

.link
  cursor: pointer

.invoice-field
  margin-left: -10px
  margin-right: -10px
  padding: 10px
  &__label
    width: 300px
    font-weight: 600
  &:nth-child(even)
    background-color: #FCFCFC
</style>
