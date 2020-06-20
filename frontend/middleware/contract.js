import _ from "lodash";

export default async function({ store }) {
  if (_.isEmpty(store.getters["contract/SIMBA"])) {
    await store.dispatch("contract/fetchContract");
  }
}
