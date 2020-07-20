<template lang="pug">
  div.main-content
    h1.title.is-size-4 User by ID — {{this.$route.params.id}}
</template>

<script>
import formatDate from "~/mixins/formatDate";
import formatCurrency from "~/mixins/formatCurrency";
export default {
  name: "usersById",
  layout: "main",
  middleware: ["adminRequired"],
  mixins: [formatDate, formatCurrency],
  computed: {
    invoiceById() {
      return this.$store.getters['users/userById']
    }
  },
  created() {
    this.$store.dispatch("users/fetchUserById", this.$route.params.id);
  }
};
</script>

<style lang="scss"></style>
