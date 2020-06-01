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
    if (!data) return false;
    return await this.$axios
      .post("/account/signup/", data)
      .then(resp => {
        this.$axios.setToken(resp.data.token, "Bearer");
        this.$cookies.set("token", resp.data.token, {
          path: "/",
          maxAge: 60 * 60 * 24 * 7
        });
        commit("setUser", resp.data.user);
        return null;
      })
      .catch(_ => {
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
