<template lang="pug">
  b-table(:data="tableData" hoverable :loading="loading" striped)
        template(slot-scope="props")
          b-table-column(field="date" label="Date" sortable width="50") {{timestampToDate(props.row.timeStamp)}}
          b-table-column(field="address" label="Address" width="70").has-text-primary.overflow-reset
            b-tooltip(:label="props.row.from" type="is-black" position="is-bottom").w-100
              a(:href="'https://etherscan.io/address/' + props.row.from" target="_blank").text-clamp {{ props.row.from }}
          b-table-column(field="txHash" label="TxHash" width="70").has-text-primary.overflow-reset
            b-tooltip(:label="props.row.hash" type="is-black" position="is-bottom").w-100
              a(:href="'https://etherscan.io/tx/' + props.row.hash" target="_blank").text-clamp {{ props.row.hash }}
          b-table-column(field="type" label="Type" width="50") Sent
          b-table-column(field="amount" label="Amount, SIMBA" width="50") {{props.row.value}}
</template>

<script>
import formatDate from '~/mixins/formatDate'
export default {
  mixins: [formatDate],
  data() {
    return {
      loading: false,
      tableData: []
    };
  },
  async created() {
    this.loading = true;
    await this.$axios
      .get(
        `https://cors-anywhere.herokuapp.com/http://api-rinkeby.etherscan.io/api?module=account&action=tokentx&address=${window.ethereum.selectedAddress}&startblock=0&endblock=999999999&sort=asc&apikey=HSZVFZ1WQ255V3CIJYSPVI3PB3BGSSIYAH`
      )
      .then(res => {
        this.loading = false;
        this.tableData = res.data.result.filter(
          el =>
            el.contractAddress === "0x60e1bf648580aafbff6c1bc122bb1ae6be7c1352"
        );
        console.log(this.tableData);
      });
  }
};
</script>

<style lang="scss" scoped>
.text-right {
  text-align: right;
}

td {
  height: 40px;
}
</style>
