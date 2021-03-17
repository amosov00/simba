export const state = () => ({
  KYCtoken: ''
})
export const getters = {
  KYCtoken: (s) => s.KYCtoken,
}
export const mutations = {
  setKYCtoken: (state, payload) => (state.KYCtoken = payload),
}
export const actions = {
  async fetchKYCtoken({ commit }) {
    const { data } = await this.$axios.get('/account/kyc/token/')
    commit('setKYCtoken', data.token)
  },
  async fetchUserData() {
    return await this.$axios.get('/account/user/')
  },
}
