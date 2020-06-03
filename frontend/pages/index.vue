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
  }
};
</script>

<style lang="sass" scoped>
</style>
