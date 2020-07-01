import Web3 from "web3";

export default ({ app, store }, inject) => {
  inject("contract", () => {
    if (!app._contract) {
      const SIMBA = store.getters["contract/SIMBA"];
      const web3 = new Web3(SIMBA.provider_http_link);
      app._contract = {
        SIMBA: new web3.eth.Contract(SIMBA.abi, SIMBA.address),
      };
    }
    return app._contract;
  });
};
