<template lang="pug">
  div.main-content
    h1.title.is-size-4 Users
    b-table(:data="users" default-sort="_id" paginated per-page="20" default-sort-direction="asc")
      template(slot-scope="props")
        b-table-column(field="_id" label="ID" width="50" sortable)
          nuxt-link(:to="`/users/${props.row._id}`") {{ props.row._id }}
        b-table-column(field="first_name" label="First name" width="50" sortable) {{ props.row.first_name }}
        b-table-column(field="last_name" label="Last name" width="50" sortable) {{ props.row.last_name }}
        b-table-column(field="email" label="Email" width="50" sortable) {{ props.row.email }}

</template>

<script>
  export default {
    name: "users",
    layout: "main",
    middleware: ["adminRequired"],
    async asyncData({store}) {
      const res = await store.dispatch("fetchUsers")

      return {
        users: res
      }
    }
  };
</script>

<style lang="scss"></style>
