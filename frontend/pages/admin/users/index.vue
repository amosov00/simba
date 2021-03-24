<template lang="pug">
    div.main-content
        div.flex.justify-content-between.mb-3
          h1.is-size-4 {{$t('su_users.users')}} (total: {{ users.length }})
          button.btn(@click="exportUsers") Export
        div.mb-3
            b-input(v-model="searchQuery" @input="onSearchInput" :placeholder="`${this.$i18n.t('other.search')}...`" icon="magnify")
        div(v-if="users.length <= 0") {{ $t('other.search_empty_results') }}
        b-table(v-if="users.length > 0" :data="users" paginated per-page="20" searchable).users-table
            template(slot-scope="props")
                b-table-column(field="_id" label="ID" width="50" sortable)
                    nuxt-link(:to="`/admin/users/${props.row._id}`") {{ props.row._id }}
                b-table-column(field="first_name" :label="$i18n.t('account_page.first_name')" width="50" sortable) {{ props.row.first_name }}
                b-table-column(field="last_name" :label="$i18n.t('account_page.last_name')" width="50" sortable) {{ props.row.last_name }}
                b-table-column(field="email" label="Email" width="50" sortable) {{ props.row.email }}
                b-table-column(field="created_at" label="Created at" width="80" sortable) {{ toDatetime(props.row.created_at) }}

</template>

<script>
import {mapState, mapActions} from 'vuex'
import _ from 'lodash'
import moment from 'moment'
// import {saveAs} from 'file-saver';

export default {
  name: 'users',
  layout: 'main',
  middleware: ['adminRequired'],
  data: () => ({
    searchQuery: '',
  }),
  computed: {
    ...mapState('admin', ['users']),
  },
  methods: {
    ...mapActions('admin', ['fetchUsers', 'exportUsers']),
    toDatetime(utc) {
      return moment.utc(utc).format('HH:mm DD-MM-YY')
    },
    onSearchInput: _.debounce(async function () {
      this.users = await this.fetchUsers(this.searchQuery.toLowerCase().trim())
    }, 500),
    async exportUsers() {
      const data = await this.exportUsers()
      if (data) {
        // saveAs(data, `simba_users.xlsx`)
      }
    },
  },
  async created() {
    if (this.users.length === 0) {
      await this.fetchUsers()
    }
  },
}
</script>

<style lang="sass">
.users-table
    .table-wrapper
        min-height: 300px

.flex
  display: flex

.justify-content-between
  justify-content: space-between
</style>
