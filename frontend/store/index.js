import _ from "lodash";

export const state = () => ({
  user: null,
});

export const getters = {
  user: s => s.user,
};

export const mutations = {
  setUser: (state, user) => (state.user = user),
  deleteUser: state => (state.user = null),
};

export const actions = {
  async signUp({ commit }, data) {
    console.log(data);

    if (!data) return false;
    return await this.$axios
      .post("/account/signup/", data)
      .then(resp => {
        return true;
      })
      .catch(_ => {
        return false
      });
  },
  async changeProfile({}, data) {
    return await this.$axios.put("/account/user/", data)
      .then(_ => {
        return true;
      })
      .catch(err => {
        return false;
      });
  },
  async changePassword({}, data) {
    return await this.$axios.post("/account/change_password/", data)
      .then(_ => {
        return true;
      })
      .catch(err => {
        return false;
      });
  },
};
