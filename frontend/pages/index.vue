<template>
  <h1>Hello!</h1>


</template>

<script>
export default {
  name: "index",
  component: {

  },
  data() {
    return {
      email: "",
      password: "",
      loading: false
    };
  },
  methods: {
    async login() {
      this.loading = true;
      let resp = await this.$authLogin(this.email, this.password);
      this.password = "";
      this.loading = false;
    }
  },
  async mounted() {
    console.log("API URL", process.env.NUXT_PORT)
    console.log("API URL", process.env.baseURL)
    return await this.$axios.get('/debug')
      .then(resp => {
        console.log(resp)
      }).catch(err => {
        console.log(err)
      })
  }
};
</script>

<style lang="sass" scoped>
</style>
