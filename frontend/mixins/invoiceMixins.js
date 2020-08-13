export default {
  methods: {
    truncateHash(hash, fromStart = 6, fromEnd = 12) {
      if(!hash) {
        return ''
      } else if(typeof hash !== 'string') {
        return ''
      }

      return `${hash.substring(0, fromStart)}...${hash.substring(hash.length - fromEnd)}`
    },
    findEthTransactionByEvent(invoice, eventName) {
      return invoice.eth_txs.find((el) => {
        return el.event === eventName
      })
    },
    getBlockchainLink(hash, hashType, currency) {
      const isProd = process.env.NODE_ENV === 'production';

      let eth_start_link;
      let btc_start_link;

      if(isProd) { // Prod
        if(hashType === 'tx') { // Transaction
          eth_start_link = 'https://etherscan.io/tx/'
          btc_start_link = 'https://www.blockchain.com/btc/tx/'
        } else { // Address
          eth_start_link = 'https://etherscan.io/address/'
          btc_start_link = 'https://www.blockchain.com/btc/address/'
        }
      } else { // Dev
        if(hashType === 'tx') { // Transaction
          eth_start_link = 'https://rinkeby.etherscan.io/tx/'
          btc_start_link = 'https://www.blockchain.com/btc-testnet/tx/'
        } else { // Address
          eth_start_link = 'https://rinkeby.etherscan.io/address/'
          btc_start_link = 'https://www.blockchain.com/btc-testnet/address/'
        }
      }

      if(currency === 'eth') {
        return eth_start_link + hash
      } else if (currency === 'btc'){
        return btc_start_link + hash
      } else {
        return '#errhash'
      }
    }
  }
}
