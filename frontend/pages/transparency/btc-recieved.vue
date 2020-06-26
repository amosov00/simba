<template lang="pug">
  div
    div.main-content
      h1.title.is-size-4 Transparency
      p.title.is-size-5 Received by Storage
      section
        b-table(:data="tableData" hoverable striped)
          template(slot-scope="props")
            b-table-column(field="date" label="Date" sortable width="50") {{props.row.date}}
            b-table-column(field="txHash" label="TxHash" width="70").has-text-primary.overflow-reset
              b-tooltip(:label="props.row.transactionHash" type="is-black" position="is-bottom").w-100
                a(:href="'https://explorer.bitcoin.com/btc/tx/' + props.row.transactionHash" target="_blank" rel="noopener").text-clamp {{ props.row.transactionHash }}
            b-table-column(field="amount" label="Amount, BTC" width="100") {{props.row.amount}}
        div.text-center
          button.btn--outlined.mt-4 more
</template>

<script>
export default {
  name: "contacts",
  layout: "main",
  data() {
    return {};
  },
  computed: {
    tableData() {
      return [
        {
          date: "01/06/2020, 09:49:15",
          transactionHash:
            "3f095787422746cd026f5a49974096083fe0b3c47e209ed0d1988b1b16fe35b6",
          amount: 116.1005
        },
        {
          date: "01/06/2020, 09:49:15",
          transactionHash:
            "3f095787422746cd026f5a49974096083fe0b3c47e209ed0d1988b1b16fe35b6",
          amount: 116.1005
        },
        {
          date: "01/06/2020, 09:49:15",
          transactionHash:
            "3f095787422746cd026f5a49974096083fe0b3c47e209ed0d1988b1b16fe35b6",
          amount: 116.1005
        },
        {
          date: "01/06/2020, 09:49:15",
          transactionHash:
            "3f095787422746cd026f5a49974096083fe0b3c47e209ed0d1988b1b16fe35b6",
          amount: 116.1005
        },
        {
          date: "01/06/2020, 09:49:15",
          transactionHash:
            "3f095787422746cd026f5a49974096083fe0b3c47e209ed0d1988b1b16fe35b6",
          amount: 116.1005
        },
        {
          date: "01/06/2020, 09:49:15",
          transactionHash:
            "3f095787422746cd026f5a49974096083fe0b3c47e209ed0d1988b1b16fe35b6",
          amount: 116.1005
        },
        {
          date: "01/06/2020, 09:49:15",
          transactionHash:
            "3f095787422746cd026f5a49974096083fe0b3c47e209ed0d1988b1b16fe35b6",
          amount: 116.1005
        },
        {
          date: "01/06/2020, 09:49:15",
          transactionHash:
            "3f095787422746cd026f5a49974096083fe0b3c47e209ed0d1988b1b16fe35b6",
          amount: 116.1005
        },
        {
          date: "01/06/2020, 09:49:15",
          transactionHash:
            "3f095787422746cd026f5a49974096083fe0b3c47e209ed0d1988b1b16fe35b6",
          amount: 116.1005
        },
        {
          date: "01/06/2020, 09:49:15",
          transactionHash:
            "3f095787422746cd026f5a49974096083fe0b3c47e209ed0d1988b1b16fe35b6",
          amount: 116.1005
        },
        {
          date: "01/06/2020, 09:49:15",
          transactionHash:
            "3f095787422746cd026f5a49974096083fe0b3c47e209ed0d1988b1b16fe35b6",
          amount: 116.1005
        },
        {
          date: "01/06/2020, 09:49:15",
          transactionHash:
            "3f095787422746cd026f5a49974096083fe0b3c47e209ed0d1988b1b16fe35b6",
          amount: 116.1005
        },
        {
          date: "01/06/2020, 09:49:15",
          transactionHash:
            "3f095787422746cd026f5a49974096083fe0b3c47e209ed0d1988b1b16fe35b6",
          amount: 116.1005
        },
        {
          date: "01/06/2020, 09:49:15",
          transactionHash:
            "3f095787422746cd026f5a49974096083fe0b3c47e209ed0d1988b1b16fe35b6",
          amount: 116.1005
        },
        {
          date: "01/06/2020, 09:49:15",
          transactionHash:
            "3f095787422746cd026f5a49974096083fe0b3c47e209ed0d1988b1b16fe35b6",
          amount: 116.1005
        },
        {
          date: "01/06/2020, 09:49:15",
          transactionHash:
            "3f095787422746cd026f5a49974096083fe0b3c47e209ed0d1988b1b16fe35b6",
          amount: 116.1005
        },
        {
          date: "01/06/2020, 09:49:15",
          transactionHash:
            "3f095787422746cd026f5a49974096083fe0b3c47e209ed0d1988b1b16fe35b6",
          amount: 116.1005
        },
        {
          date: "01/06/2020, 09:49:15",
          transactionHash:
            "3f095787422746cd026f5a49974096083fe0b3c47e209ed0d1988b1b16fe35b6",
          amount: 116.1005
        },
        {
          date: "01/06/2020, 09:49:15",
          transactionHash:
            "3f095787422746cd026f5a49974096083fe0b3c47e209ed0d1988b1b16fe35b6",
          amount: 116.1005
        },
        {
          date: "01/06/2020, 09:49:15",
          transactionHash:
            "3f095787422746cd026f5a49974096083fe0b3c47e209ed0d1988b1b16fe35b6",
          amount: 116.1005
        },
        {
          date: "01/06/2020, 09:49:15",
          transactionHash:
            "3f095787422746cd026f5a49974096083fe0b3c47e209ed0d1988b1b16fe35b6",
          amount: 116.1005
        },
        {
          date: "01/06/2020, 09:49:15",
          transactionHash:
            "3f095787422746cd026f5a49974096083fe0b3c47e209ed0d1988b1b16fe35b6",
          amount: 116.1005
        },
        {
          date: "01/06/2020, 09:49:15",
          transactionHash:
            "3f095787422746cd026f5a49974096083fe0b3c47e209ed0d1988b1b16fe35b6",
          amount: 116.1005
        },
        {
          date: "01/06/2020, 09:49:15",
          transactionHash:
            "3f095787422746cd026f5a49974096083fe0b3c47e209ed0d1988b1b16fe35b6",
          amount: 116.1005
        }
      ];
    }
  }
};
</script>

<style lang="sass" scoped></style>
