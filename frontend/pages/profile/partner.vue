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
    div.mt-4.mb-2(v-html="$t('partner.main')").main-content__text
    div.has-text-weight-bold.is-size-5.mt-4 {{$t('partner.invited')}}
    b-table(:data="referrals" focusable striped).mt-3
      template(slot="empty")
        div.content.has-text-grey.has-text-centered {{$t('partner.refs_empty')}}
      template(slot-scope="props")
        b-table-column(field="created_at" :label="$i18n.t('other.reg_date')") {{ formatDate(props.row.created_at) }}
        b-table-column(field="ref_email" label="Email") {{ props.row.email }}
        b-table-column(field="name" :label="$i18n.t('other.name')") {{ props.row.first_name }} {{ props.row.last_name }}
        b-table-column(field="referral_level" :label="$i18n.t('other.level')") {{ props.row.referral_level }}
    div.has-text-weight-bold.is-size-5.mt-4 {{$t('wallet.txs_history')}}
    b-table(:data="[]" focusable striped).mt-3
      template(slot="empty")
        div.content.has-text-grey.has-text-centered {{$t('wallet.txs_history_empty')}}
    //--div.text-center
      button.btn--outlined(@click="history_more_data += 10") {{$t('other.more')}}
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
