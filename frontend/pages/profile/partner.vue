<template lang="pug">
  div
    div.is-size-5.has-text-weight-bold {{ $t('partner.your_ref_code')}}:
    div.is-flex.mt-3
      div.mr-2.has-text-weight-medium {{ ref_code }}
      CopyToClipboard(:value_to_copy="ref_code")
    div.mt-4
      div.is-size-5.has-text-weight-bold {{ $t('partner.your_ref_link')}}:
      div.is-flex.mt-2
        div.mr-2.has-text-weight-medium
          a(:href="ref_link").link {{ ref_link }}
        CopyToClipboard(:value_to_copy="ref_link")
    div.mt-4.mb-2(v-html="$t('partner.main')").is-size-6
    div.has-text-weight-bold.is-size-5.mt-4 {{$t('partner.invited')}}
    b-table(:data="table1.data" focusable striped).mt-3
      template(slot-scope="props")
        b-table-column(field="date" :label="$i18n.t('other.reg_date')") {{ props.row.date }}
        b-table-column(field="email" email="Email") {{ props.row.email }}
        b-table-column(field="name" :label="$i18n.t('other.name')") {{ props.row.name }}
        b-table-column(field="level" :label="$i18n.t('other.level')") {{ props.row.level }}
    div.has-text-weight-bold.is-size-5.mt-4 {{$t('wallet.txs_history')}}
    WalletTable(:moreData="history_more_data").mt-3
    div.text-center
      button.btn--outlined(@click="history_more_data += 10") {{$t('other.more')}}
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
      },
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
