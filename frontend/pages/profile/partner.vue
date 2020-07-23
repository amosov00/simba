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
      div.column.has-text-right
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
          b-table-column(field="ref_email" label="Email") {{ props.row.email }}
          b-table-column(field="transactionHash" label="TxHash" width="100").has-text-primary.overflow-reset
            b-tooltip(:label="props.row.transactionHash" type="is-black" position="is-bottom")
              a(:href="'https://etherscan.io/tx/' + props.row.transactionHash" target="_blank").text-clamp {{ props.row.transactionHash }}

          //- b-table-column(field="txHash" label="txHash")
            b-tooltip(:label="props.row.transactionHash" type="is-black" position="is-bottom")
              a(:href="'https://etherscan.io/tx/' + props.row.transactionHash" target="_blank") {{ props.row.transactionHash }}
          b-table-column(field="referral_level" :label="$i18n.t('other.level')") {{ props.row.referral_level }}
          b-table-column(field="Amount" label="Amount") {{ props.row.amount }}
      div.level.mt-4
        p.is-size-5.has-text-weight-bold.level-left Total
        p.is-size-5.has-text-weight-bold.level-right {{txTotal}}
</template>

<script>

  import CopyToClipboard from "~/components/CopyToClipboard";

  import WalletTable from "~/components/WalletTable";

  import moment from 'moment'

  export default {
    name: "profile-partner",
    layout: "profile",
    components: { CopyToClipboard, WalletTable },
    middleware: ["contract", "metamask"],
    computed: {
      codeUnavailable() {
        if(this.ref_code.includes('*')) {
          return true
        }
        else {
          return false
        }
      },
      rewardAddress() {
        return this.$store.getters.user.user_eth_addresses[0].address
      },
      txTotal() {
        return this.transactions.reduce((total, el) => {
          return total + el.amount
        }, 0)
      }
    },
    data: () => ({
      ref_code: '',
      history_more_data: 5,
      referrals: []
    }),
    methods: {
      formatDate(date_str) {
        return moment(String(date_str)).format(("DD/MM/YYYY, h:mm:ss"))
      },

      setTextRefLink() {
        if(this.ref_link) {
          document.getElementById('text-ref-link').setAttribute('href', this.ref_link)
        }
      }
    },

    created() {
      this.formatDate()

      if(this.ref_link) {
        let url_data = new URL(this.ref_link)
        this.ref_code = url_data.searchParams.get("referral_id")
      }
    },

    mounted() {
      this.setTextRefLink();
    },

    updated() {
      this.setTextRefLink();
    },

    async asyncData({store}) {

      let ref_link = await store.dispatch('fetchRefLink');
      let referrals = await store.dispatch('fetchReferrals');
      let transactions = await store.dispatch('fetchTransactions');

      let result = {
        can_invite: false
      }

      if(store.getters.user.user_eth_addresses.length) {
        result['can_invite'] = true
      }

      if(ref_link) {
        result['ref_link'] = ref_link.URL
      }

      if(referrals) {
        result['referrals'] = referrals
      }

      if(transactions) {
        result['transactions'] = transactions
      }

      return result
    }
  };
</script>

<style lang="sass" scoped>
.w-100
  width: 100%
.overflow-reset
  &:hover
    overflow: initial!important
.text-clamp
  overflow: hidden
  text-overflow: ellipsis

</style>
