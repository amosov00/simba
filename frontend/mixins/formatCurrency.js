export default {
  methods: {
    simbaFormat(value) {
      return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
    },
    sstFormat(value) {
      return (value / 10 ** 18).toFixed(2)
    },
    btcFormat(value) {
      return (value / 10 ** 8).toFixed(4)
    },
  },
}
