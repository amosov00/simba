import Web3 from "web3";

function getWeb3(infuraURL) {
  let web3 = null

  if (window?.ethereum && window.ethereum.chainId === "0x1") {
    if (
      (process.env.ENV === "production" && window.ethereum.chainId === "0x1") ||
      (process.env.ENV !== "production" && window.ethereum.chainId === "0x4")
    ) {
      try {
        web3 = new Web3(window.ethereum)
      } catch (e) {
        console.error(e)
      }
    }
  }

  if (!web3) {
    web3 = new Web3(infuraURL)
  }
  return web3
}

export default ({app, store}, inject) => {
  inject("contract", () => {
    if (!app._contract) {
      const SIMBA = store.getters["contract/SIMBA"];
      const providerWSLink = store.getters["contract/providerWSLink"];
      const web3 = getWeb3(providerWSLink);

      app._contract = {
        SIMBA: new web3.eth.Contract(SIMBA.abi, SIMBA.address),
      };
    }
    return app._contract;
  });
};
