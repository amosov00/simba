<template lang="pug">
  b-table(:data="tableData" hoverable striped)
        template(slot-scope="props")
          b-table-column(field="date" label="Date" sortable width="50") {{props.row.date}}
          b-table-column(field="address" label="Address" width="70").has-text-primary.overflow-reset
            b-tooltip(:label="props.row.address" type="is-black" position="is-bottom").w-100
              a(:href="'https://etherscan.io/address/' + props.row.address" target="_blank").text-clamp {{ props.row.address }}
          b-table-column(field="txHash" label="TxHash" width="70").has-text-primary.overflow-reset
            b-tooltip(:label="props.row.transactionHash" type="is-black" position="is-bottom").w-100
              a(:href="'https://etherscan.io/tx/' + props.row.transactionHash" target="_blank").text-clamp {{ props.row.transactionHash }}
          b-table-column(field="type" label="Type" width="50") {{props.row.type}}
          b-table-column(field="amount" label="Amount, SIMBA" width="50") {{props.row.amount}}
</template>

<script>
export default {
  data() {
    return {};
  },
  computed: {
    tableData() {
      return [
        {
          date: "12/06/2020",
          address: "0xd69401E5B2F93EB66E585711ec4CEFD6e8C8346D",
          transactionHash: "0xd69401E5B2F93EB66E585711ec4CEFD6e8C8346D",
          type: "Sent",
          amount: 116000000
        },
        {
          date: "12/06/2020",
          address: "0xd69401E5B2F93EB66E585711ec4CEFD6e8C8346D",
          transactionHash: "0xd69401E5B2F93EB66E585711ec4CEFD6e8C8346D",
          type: "Sent",
          amount: 116000000
        },
        {
          date: "12/06/2020",
          address: "0xd69401E5B2F93EB66E585711ec4CEFD6e8C8346D",
          transactionHash: "0xd69401E5B2F93EB66E585711ec4CEFD6e8C8346D",
          type: "Sent",
          amount: 116000000
        },
        {
          date: "12/06/2020",
          address: "0xd69401E5B2F93EB66E585711ec4CEFD6e8C8346D",
          transactionHash: "0xd69401E5B2F93EB66E585711ec4CEFD6e8C8346D",
          type: "Sent",
          amount: 116000000
        }
      ];
    }
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
