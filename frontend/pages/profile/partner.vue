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
    div.mt-4.mb-2.is-size-6 Get tokens for each deposit of users invited via your link. How it works?
    div.is-size-6
      div 1. You copy the link and send it to your friend.
      div 2. After sign up with your link, it will be tied to your account.
      div 3. With each recharge, you will receive SST tokens that you can sell on an exchange at the current rate.
      div The offer is limited by amount of provided SST tokens.
    div.has-text-weight-bold.is-size-5.mt-4 Invited
    b-table(:data="table1.data" :columns="table1.columns" focusable striped).mt-3
    div.has-text-weight-bold.is-size-5.mt-4 History of transactions
    b-table(:data="table2.data" :columns="table2.columns" focusable striped).mt-3
      template(slot="footer")
        div.is-flex.space-between.has-text-weight-bold.mt-3
          div Total
          div 999,232,050.50
</template>

<script>

  import CopyToClipboard from "~/components/CopyToClipboard";

  export default {
    name: "profile-partner",
    layout: "profile",
    components: { CopyToClipboard },
    computed: {
    },
    data: () => ({
      ref_code: '',
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
      let res = await store.dispatch('fetchRefLink');

      if(store.dispatch('fetchRefLink')) {
        return { ref_link: res.URL }
      }
    }
  };
</script>

<style lang="sass" scoped></style>
