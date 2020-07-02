<template lang="pug">
  div
    div.is-size-5.has-text-weight-bold Your referral code:
    div.is-flex.mt-2
      div.mr-2.has-text-weight-medium {{ ref_code }}
      CopyToClipboard(:value_to_copy="ref_code")
    div.mt-3
      div.is-size-5.has-text-weight-bold Your referral link:
      div.is-flex.mt-2
        div.mr-2.has-text-weight-medium
          a(:href="ref_link").link {{ ref_link }}
        CopyToClipboard(:value_to_copy="ref_link")
    div.mt-4.mb-2(v-html="$t('partner.main')").is-size-6
    div.has-text-weight-bold.is-size-5.mt-4 Invited
    b-table(:data="table1.data" :columns="table1.columns" focusable striped).mt-3
    //--  template(slot-scope="props")
        b-table-column field="id" label="ID" width="40" numeric {{ props.row.id }}
    div.has-text-weight-bold.is-size-5.mt-4 History of transactions
    WalletTable(:moreData="history_more_data").mt-3
    div.text-center
      button.btn--outlined(@click="history_more_data += 10") more
    //--b-table(:data="table2.data" :columns="table2.columns" focusable striped).mt-3
      template(slot="footer")
        div.is-flex.space-between.has-text-weight-bold.mt-3
          div Total
          div 999,232,050.50
</template>

<script>

  import CopyToClipboard from "~/components/CopyToClipboard";

  import WalletTable from "~/components/WalletTable";

  export default {
    name: "profile-partner",
    layout: "profile",
    components: { CopyToClipboard, WalletTable },
    middleware: ["contract", "metamask"],
    computed: {
    },
    data: () => ({
      ref_code: '',
      history_more_data: 5,
      table1: {
        data: [
          { date: '01/06/2020, 09:49:15', email: 'example@test.test', name: 'Константин Константинопольский', level: 1},
          { date: '01/06/2020, 09:49:15', email: 'example@test.test', name: 'Константин Константинопольский', level: 2},
          { date: '01/06/2020, 09:49:15', email: 'example@test.test', name: 'Константин Константинопольский', level: 3},
        ],
        columns: [
          { label: 'Registration date', field: 'date' },  { label: 'E-mail', field: 'email' },
          { label: 'Name', field: 'name' }, { label: 'Level', field: 'level' }
        ]
      },
      table2: {
        data: [
          { date: '01/06/2020, 09:49:15', email: 'example@test.test', amount_sst: '116,000.00', level: 1},
          { date: '01/06/2020, 09:49:15', email: 'example@test.test', amount_sst: '999,000,050.00', level: 1},
          { date: '01/06/2020, 09:49:15', email: 'example@test.test', amount_sst: '116,000.50', level: 4},
        ],
        columns: [
          { label: 'Registration date', field: 'date' },  { label: 'E-mail', field: 'email' },
          { label: 'Level', field: 'level' }, { label: 'Amount, SST', field: 'amount_sst', 'cell-class': 'has-text-right'}
        ]
      }
    }),
    methods: {
    },

    created() {
      if(this.ref_link) {
        let url_data = new URL(this.ref_link)
        this.ref_code = url_data.searchParams.get("referral_id")
      }
    },

    async asyncData({store}) {
      let ref_link = await store.dispatch('fetchRefLink');
      let referrals = await store.dispatch('fetchReferrals');

      let result = {}

      if(ref_link) {
        result['ref_link'] = ref_link.URL
      }

      if(referrals) {
        result['referrals'] = referrals
      }

      return result
    }
  };
</script>

<style lang="sass" scoped></style>
