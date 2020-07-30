<template lang="pug">
  div.main-content
    div.is-size-4.mb-3
      strong {{$t('su_invoices.invoice')}}
      =' — '
      span {{this.$route.params.id}}
    div(v-for="(el, key) in invoice").is-flex.invoice-field
      div.invoice-field__label {{ $t(`su_invoices.${key}`) }}:
      div.flex-1
        div(v-if="Array.isArray(el)")
          div(v-if="el.length > 0")
            div(v-for="(item, i) in el" :key="i")
              div(v-if="typeof item === 'object'") -
                //--div(v-for="(value, key) in item") {{key}}: {{value}}
              div(v-else) {{ item }}
          div(v-else) {{ $t(`su_invoices.empty`) }}
        div(v-else)
          div(v-if="el === null") {{ $t(`su_invoices.not_available`) }}
          div(v-else)
            div(v-if="key === 'invoice_type'") {{ el === 1 ? $i18n.t('exchange.buy') : $i18n.t('exchange.sell') }}
            div(v-else-if="key === 'status'") {{ $t(`exchange.statuses.${el}`)}}
            div(v-else-if="key === 'created_at' || key === 'finised_at'") {{ timestampFromUtc(el) }}
            div(v-else-if="key === 'btc_amount_proceeded' || key === 'btc_amount'") {{ btcFormat(el) }}
            div(v-else) {{ el }}
</template>

<script>
import formatDate from "~/mixins/formatDate";
import formatCurrency from "~/mixins/formatCurrency";
export default {
  name: "invoicesById",
  layout: "main",
  middleware: ["adminRequired"],
  mixins: [formatDate, formatCurrency],

  async asyncData({store, route}) {
    const invoice = await store.dispatch('invoices/fetchAdminSingleInvoice', route.params.id)

    return {
      invoice
    }
  }
};
</script>

<style lang="sass">
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
