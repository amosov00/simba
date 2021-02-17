<template lang="pug">
  div
    div.columns
      div.column
        div.is-size-5.has-text-weight-bold {{ $t('partner.your_ref_code')}}:
        div.is-flex.mt-3
          div.has-text-weight-medium(v-if="can_invite") {{ ref_code }}
          div(v-else)
            | {{$t('partner.how_to_get_code.p1')}}
            n-link(to="/profile/bill").link {{$t('partner.how_to_get_code.p2')}}
            = ' '
            | {{$t('partner.how_to_get_code.p3')}}
          CopyToClipboard(:value_to_copy="ref_code").ml-2
      div.column.has-text-right(v-if="this.$store.getters.user.user_eth_addresses.length > 0")
        div.is-size-5.has-text-weight-bold {{ $t('partner.your_reward_address')}}:
        div.is-flex.mt-3
          div.has-text-weight-medium() {{ rewardAddress }}
          CopyToClipboard(:value_to_copy="rewardAddress").ml-2
    div.mt-4
      div.is-size-5.has-text-weight-bold {{ $t('partner.your_ref_link')}}:
      div.is-flex.mt-2
        div.mr-2.has-text-weight-medium
          a(:href="ref_link").link {{ ref_link }}
        CopyToClipboard(:value_to_copy="ref_link")
    div.mt-4.mb-2(v-html="$t('partner.main')").main-content__text
    div(v-if="can_invite")
      div.has-text-weight-bold.is-size-5.mt-4 {{$t('partner.invited')}}
      b-table(:data="referrals" focusable striped default-sort="created_at" default-sort-direction="desc" per-page="5" :paginated="Boolean(referrals.length)" pagination-simple).mt-3
        template(slot="empty")
          div.content.has-text-grey.has-text-centered {{$t('partner.refs_empty')}}
        template(slot-scope="props")
          b-table-column(field="created_at" :label="$i18n.t('other.reg_date')" sortable) {{ formatDate(props.row.created_at) }}
          b-table-column(field="ref_email" label="Email") {{ props.row.email }}
          b-table-column(field="name" :label="$i18n.t('other.name')") {{ props.row.first_name }} {{ props.row.last_name }}
          b-table-column(field="referral_level" :label="$i18n.t('other.level')") {{ props.row.referral_level }}
      div.has-text-weight-bold.is-size-5.mt-4 {{$t('wallet.txs_history')}}
      b-table(:data="transactions" focusable striped per-page="5" :paginated="true" pagination-simple).mt-3
        template(slot="empty")
          div.content.has-text-grey.has-text-centered {{$t('wallet.txs_history_empty')}}
        template(slot-scope="props")
          b-table-column(field="email" label="Email" width="200") {{ props.row.email }}
          b-table-column(field="transactionHash" label="TxHash").has-text-primary.overflow-reset
            b-tooltip(:label="props.row.transactionHash" type="is-black" position="is-bottom")
              a(:href="'https://etherscan.io/tx/' + props.row.transactionHash" target="_blank").text-clamp {{ truncateHash(props.row.transactionHash) }}
          b-table-column(field="level" :label="$i18n.t('other.level')") {{ props.row.level }}
          b-table-column(field="amount" :label="$i18n.t('other.amount')") {{ divNum(props.row.amount) }}
      div.level.mt-2
        p.is-size-5.has-text-weight-bold.level-left {{ $i18n.t('other.total')}}
        p.is-size-5.has-text-weight-bold.level-right {{ txTotal }}
</template>

<script>
import invoiceMixins from '~/mixins/invoiceMixins'

import CopyToClipboard from '~/components/CopyToClipboard'

import WalletTable from '~/components/WalletTable'

import moment from 'moment'

import { Decimal } from 'decimal.js'

export default {
  name: 'profile-partner',
  layout: 'profile',
  components: { CopyToClipboard, WalletTable },
  middleware: ['contract', 'metamask'],
  mixins: [invoiceMixins],
  computed: {
    rewardAddress() {
      return this.$store.getters.user.user_eth_addresses[0].address
    },
    txTotal() {
      let total = this.transactions.reduce((total, el) => {
        return total.plus(el.amount)
      }, Decimal(0))

      return Decimal.div(total, 10 ** 18).toFixed(2)
    },
  },
  data: () => ({
    ref_link: '',
    ref_code: '',
    history_more_data: 5,
    referrals: [],
    can_invite: false,
  }),
  methods: {
    divNum(num) {
      return (+num / 10 ** 18).toFixed(2)
    },

    formatDate(date_str) {
      return moment(String(date_str)).format('DD/MM/YYYY, h:mm:ss')
    },

    setTextRefLink() {
      if (this.ref_link) {
        document.getElementById('text-ref-link').setAttribute('href', this.ref_link)
      }
    },
  },

  created() {
    this.formatDate()
  },

  mounted() {
    this.setTextRefLink()
  },

  updated() {
    this.setTextRefLink()
  },

  async asyncData({ store }) {
    const { url, partner_code } = await store.dispatch('fetchRefLink')
    const { referrals, transactions } = await store.dispatch('fetchReferrals')

    return {
      can_invite: Boolean(store.getters.user.user_eth_addresses.length),
      ref_link: url,
      ref_code: partner_code,
      referrals: referrals,
      transactions: transactions,
    }
  },
}
</script>

<style lang="sass" scoped>
.w-100
  width: 100%

.overflow-reset
  &:hover
    overflow: initial !important

.text-clamp
  overflow: hidden
  text-overflow: ellipsis
</style>
