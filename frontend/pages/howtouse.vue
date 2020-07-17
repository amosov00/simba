<template lang="pug">
  div
    div.main-content
      Nothing
</template>

<script>
  import Nothing from "~/components/Nothing";

  export default {
    name: "howtouse",
    layout: "main",
    components: {Nothing},
    data() {
      return {
      };
    },
    methods: {
    },
    mounted() {
      console.log(process.env.NODE_ENV)
    }
  };
</script>

<style lang="sass" scoped>
</style>
