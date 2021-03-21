import { DialogProgrammatic as Dialog, ToastProgrammatic as Toast } from 'buefy'

export const state = () => ({
  user: null,
  kyc: null,
  metamaskEthAddress: '',
  contract: '',
  loginDataBuffer: {},
})

export const getters = {
  user: (s) => s.user,
  contract: (s) => s.contract,
  tradeData: (s) => s.tradeData,
  loginDataBuffer: (s) => s.loginDataBuffer,
}

export const mutations = {
  setUser: (state, user) => (state.user = user),
  setKYC: (state, payload) => (state.kyc = payload),
  deleteUser: (state) => (state.user = null),
  setContract: (state, data) => (state.contract = data),
  setMetamaskEthAddress: (state, payload) => (state.metamaskEthAddress = payload),
  setTwoFactor: (state, payload) => (state.user.two_factor = payload),
  setSignedAddresses: (state, payload) => state.user.signed_addresses.push(payload),
  setLoginDataBuffer: (state, payload) => {
    state.loginDataBuffer = payload
  },
}

export const actions = {
  async fetchReferrals() {
    return this.$axios
      .get('/account/referrals/')
      .then((res) => res.data)
      .catch(() => false)
  },

  async changeAddresses({}, data) {
    return this.$axios
      .put('/account/user/', data)
      .then(() => true)
      .catch(() => false)
  },

  async addAddress({ dispatch }, data) {
    if (data.type === 'eth') {
      try {
        await dispatch('metamask/createSignature', data)
        return true
      } catch (e) {
        Toast.open({
          message: this.$i18n.t('wallet.failed_to_get_signature'),
          type: 'is-danger',
          duration: 6000,
        })
        return false
      }
    } else {
      return this.$axios
        .post(`/account/btc-address/`, data)
        .then(() => {
          dispatch('getUser')
          Toast.open({
            message: this.$i18n.t('wallet.address_added'),
            type: 'is-primary',
          })
          return true
        })
        .catch((_) => {
          let error
          if (this.getters.user.two_factor) {
            error = this.$i18n.t('wallet.address_failed_with_pin')
          } else {
            error = this.$i18n.t('wallet.address_failed_to_add')
          }
          Toast.open({
            message: error,
            type: 'is-danger',
            duration: 6000,
          })
          return false
        })
    }
  },

  async removeAddress({ dispatch }, data) {
    if (data.type === 'btc') {
      return this.$axios
        .delete(`/account/btc-address/`, {
          data: {
            address: data.address,
            pin_code: data.pin_code,
          },
        })
        .then(() => {
          dispatch('getUser')
          Toast.open({
            message: this.$i18n.t('wallet.address_deleted'),
            type: 'is-primary',
          })
        })
        .catch((resp) => {
          Toast.open({
            message: resp.response.data[0].message,
            type: 'is-danger',
            duration: 6000,
          })
        })
    } else {
      return this.$axios
        .delete(`/account/eth-address/${data.address}`)
        .then(() => {
          dispatch('getUser')
          Toast.open({
            message: this.$i18n.t('wallet.address_deleted'),
            type: 'is-primary',
          })
        })
        .catch((resp) => {
          Toast.open({
            message: resp.response.data[0].message,
            type: 'is-danger',
            duration: 6000,
          })
        })
    }
  },

  async fetchContracts({ commit }) {
    return this.$axios
      .get('/meta/eth/contract/')
      .then((res) => {
        commit('setContract', res.data)
        return true
      })
      .catch((_) => false)
  },

  async activateAccount({}, data) {
    if (!data) return false

    return this.$axios
      .post('/account/verify/', data)
      .then((resp) => {
        return resp.data
      })
      .catch((_) => {
        return false
      })
  },

  async getUser({ commit }) {
    return this.$axios
      .get('/account/user/')
      .then((resp) => {
        if (resp.status === 200) {
          commit('setUser', resp.data)
          return true
        }

        return false
      })
      .catch((_) => false)
  },

  async fetchRefLink({}) {
    return this.$axios
      .get('/account/referral_link/')
      .then((resp) => {
        if (resp.status === 200) {
          return resp.data
        }
        return false
      })
      .catch((_) => false)
  },

  async signUp({ commit }, data) {
    if (!data) return false
    return this.$axios
      .post('/account/signup/', data)
      .then((resp) => {
        Toast.open({
          message: this.$i18n.t('auth.sign_up_success'),
          type: 'is-primary',
          duration: 6000,
        })
        return true
      })
      .catch((resp) => {
        if (resp.response.data[0].message === 'Referral link invalid') {
          Dialog.alert({
            message: `${this.$i18n.t(
              'auth.sign_up_error_referral'
            )} <a href='mailto:support@simba.storage'>${this.$i18n.t('auth.to_support')}</a>`,
            type: 'is-primary',
          })
        } else {
          Toast.open({
            message: resp.response.data[0].message,
            type: 'is-danger',
            duration: 6000,
          })
        }
        return false
      })
  },
  async changePassword({}, data) {
    return this.$axios
      .post('/account/change_password/', data)
      .then((_) => {
        return true
      })
      .catch((err) => {
        return false
      })
  },
  async startRecover({}, data) {
    return this.$axios
      .post('/account/recover/', data)
      .then((_) => {
        return true
      })
      .catch((err) => {
        return false
      })
  },
  async finishRecover({}, data) {
    return this.$axios
      .put('/account/recover/', data)
      .then((_) => {
        return true
      })
      .catch((err) => {
        return false
      })
  },
  async confirm2fa({ commit }, data) {
    return this.$axios
      .post('/account/2fa/', {
        token: data.token,
        pin_code: data.pin_code,
      })
      .then(() => {
        commit('setTwoFactor', true)
        Toast.open({
          message: this.$i18n.t('messages.two_factor_enable_success'),
          type: 'is-primary',
        })
      })
      .catch(() => {
        Toast.open({
          message: this.$i18n.t('messages.two_factor_enable_failed'),
          type: 'is-danger',
        })
      })
  },
  async delete2fa({ commit }, pin_code) {
    return this.$axios
      .delete('/account/2fa/', {
        data: {
          pin_code: `${pin_code}`,
        },
      })
      .then(() => {
        commit('setTwoFactor', false)
        Toast.open({
          message: this.$i18n.t('messages.two_factor_disable_success'),
          type: 'is-primary',
        })
      })
      .catch(() => {
        Toast.open({
          message: this.$i18n.t('messages.two_factor_disable_failed'),
          type: 'is-danger',
        })
      })
  },
  async getKYCStatus({ commit }) {
    return this.$axios
      .get('/account/kyc/status/')
      .then((resp) => {
        if (resp.status === 200) {
          commit('setKYC', resp.data)
          return true
        }
        return false
      })
      .catch((_) => false)
  },
  async getKYCToken({ commit }) {
    return this.$axios
      .get('/account/kyc/token/')
      .then((resp) => {
        if (resp.status === 200) {
          return resp.data.token
        }
        return false
      })
      .catch((_) => false)
  },
}
