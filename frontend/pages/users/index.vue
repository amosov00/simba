<template lang="pug">
  div.main-content
    h1.title.is-size-4 Users
    div.mb-3
      b-input(v-model="searchQuery" @input="onSearchInputWrapper" placeholder="Поиск..." icon="magnify")
    div(v-if="usersToView.length <= 0") Пользователей не найдено
    b-table(:data="usersToView" default-sort="_id" paginated per-page="20" default-sort-direction="asc" searchable).users-table
      template(slot-scope="props")
        b-table-column(field="_id" label="ID" width="50" sortable)
          nuxt-link(:to="`/users/${props.row._id}`") {{ props.row._id }}
        b-table-column(field="first_name" label="First name" width="50" sortable) {{ props.row.first_name }}
        b-table-column(field="last_name" label="Last name" width="50" sortable) {{ props.row.last_name }}
        b-table-column(field="email" label="Email" width="50" sortable) {{ props.row.email }}

</template>

<script>

  import _ from 'lodash'

  export default {
    name: "users",
    layout: "main",
    middleware: ["adminRequired"],
    data: () => ({
      usersCache: [],
      usersToView: [],
      searchQuery: '',
    }),

    mounted() {
      console.log(this.usersCache === this.usersToView)
    },

    methods: {

      onSearchInputWrapper() {
        this.onSearchInput()
      },

      onSearchInput: _.debounce(function() {
        if(this.searchQuery !== '' || this.searchQuery.length <= 0) {
          this.usersToView = this.usersCache.filter(el => {
            for(let key in el){
              if(String(el[key]).toLowerCase().includes(this.searchQuery.toLowerCase())) {
                return true
              }
            }
            return false
          })
        } else {
          this.usersToView = this.usersCache
        }
      }, 500)
    },

    async asyncData({store}) {
      const res = await store.dispatch("fetchUsers")
      return {
        usersCache: res,
        usersToView: res
      }
    }
  };
</script>

<style lang="sass">
  .users-table
    .table-wrapper
      min-height: 300px
</style>
