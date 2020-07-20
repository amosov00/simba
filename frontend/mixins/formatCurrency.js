export default {
  methods: {
    simbaFormat(value) {
      return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    },
    btcFormat(value) {
      return (value / 100000000).toFixed(4);
    }
  }
};
