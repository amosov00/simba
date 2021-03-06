<template lang="pug">
  div
    b-table(:data="cuttedData" hoverable :loading="loading" striped :class="{'loading-height': loading}").table-fixed.position-relative
      template(slot="empty")
        div.content.has-text-grey.has-text-centered(v-if="!loading") {{$t('wallet.txs_history_empty')}}
      template(slot-scope="props")
        b-table-column(field="timeStamp" :label="$i18n.t('other.date')" width="100") {{timestampToDate(props.row.timeStamp)}}
        b-table-column(field="address" :label="$i18n.t('other.address')").overflow-reset
          b-tooltip(:label="props.row.from" type="is-primary" position="is-bottom").w-100
            a(:href="'https://etherscan.io/address/' + props.row.from" target="_blank").text-clamp {{ props.row.from }}
        b-table-column(field="txHash" label="TxHash").overflow-reset
          b-tooltip(:label="props.row.hash" type="is-primary" position="is-bottom").w-100
            a(:href="'https://etherscan.io/tx/' + props.row.hash" target="_blank").text-clamp {{ props.row.hash }}
        b-table-column(field="type" :label="$i18n.t('other.type')") {{$t('other.sent')}}
        b-table-column(field="amount" :label="$i18n.t('other.amount') + ', SIMBA'" header-class="column-header-right").text-right {{simbaFormat(props.row.value)}}
      template(slot="footer")
        div(v-if="cuttedData.length > 0").is-flex.space-between.has-text-weight-bold.mt-3
          div {{ $t('other.total')}}
          div {{ total }}
    div.mt-3.text-center
      button.btn--outlined(@click="moreData += 10" v-if="showMoreBtn" ) {{$t('other.more')}}
</template>

<script>
import formatDate from '~/mixins/formatDate'
import formatCurrency from '~/mixins/formatCurrency'
export default {
  name: 'WalletTable',
  mixins: [formatDate, formatCurrency],
  data() {
    return {
      loading: false,
      tableData: [],
      cuttedData: [],
      total: '',
      moreData: 5,
      showMoreBtn: true,
    }
  },
  watch: {
    moreData: function () {
      if (this.tableData.length <= this.moreData) {
        this.showMoreBtn = false
      }

      this.cuttedData = this.tableData.slice(0, this.moreData)
    },
  },
  async created() {
    if (window.ethereum === undefined) {
      this.showMoreBtn = false
      return
    }

    this.loading = true
    let networkAPI
    if (this.$store.getters['contract/SIMBA'].is_test) {
      networkAPI = 'api-rinkeby'
    } else {
      networkAPI = 'api'
    }
    await this.$axios
      .get(
        `https://cors-anywhere.herokuapp.com/http://${networkAPI}.etherscan.io/api?module=account&action=tokentx&address=${window.ethereum.selectedAddress}&startblock=0&endblock=999999999&sort=desc&apikey=HSZVFZ1WQ255V3CIJYSPVI3PB3BGSSIYAH`,
        { timeout: 30 * 1000 }
      )
      .then((res) => {
        this.tableData = res.data.result.filter(
          (el) => el.contractAddress === '0x60e1bf648580aafbff6c1bc122bb1ae6be7c1352'
        )
        this.total = this.tableData.reduce((sum, current) => {
          return +sum + +current.value
        }, 0)

        this.total = this.total ? this.simbaFormat(this.total) : ''
        this.cuttedData = this.tableData.slice(0, this.moreData)
        this.loading = false
      })
      .catch(() => {
        this.showMoreBtn = false
        this.cuttedData = []
        this.loading = false
      })
  },
}
</script>

<style lang="scss" scoped>
.text-right {
  text-align: right;
}

td {
  height: 40px;
  word-break: break-all;
}

.word-break-all {
  word-break: break-all;
}

.loading-height {
  min-height: 200px;
}
</style>
