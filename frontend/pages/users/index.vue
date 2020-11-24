<template lang="pug">
    div.main-content
        h1.title.is-size-4 {{$t('su_users.users')}}
        div.mb-3
            b-input(v-model="searchQuery" @input="onSearchInput" :placeholder="`${this.$i18n.t('other.search')}...`" icon="magnify")
        div(v-if="usersToView.length <= 0") {{ $t('other.search_empty_results') }}
        b-table(v-if="usersToView.length > 0" :data="usersToView" paginated per-page="20" searchable).users-table
            template(slot-scope="props")
                b-table-column(field="_id" label="ID" width="50" sortable)
                    nuxt-link(:to="`/users/${props.row._id}`") {{ props.row._id }}
                b-table-column(field="first_name" :label="$i18n.t('account_page.first_name')" width="50" sortable) {{ props.row.first_name }}
                b-table-column(field="last_name" :label="$i18n.t('account_page.last_name')" width="50" sortable) {{ props.row.last_name }}
                b-table-column(field="email" label="Email" width="50" sortable) {{ props.row.email }}
                b-table-column(field="created_at" label="Created at" width="80" sortable) {{ toDatetime(props.row.created_at) }}

</template>

<script>
import _ from 'lodash'
import moment from "moment"

export default {
    name: "users",
    layout: "main",
    middleware: ["adminRequired"],
    data: () => ({
        usersCache: [],
        usersToView: [],
        searchQuery: '',
    }),

    methods: {
        toDatetime(utc) {
            return moment.utc(utc).format("HH:mm DD-MM-YY")
        },
        onSearchInput: _.debounce(function () {
            let properSearchQuery = this.searchQuery.toLowerCase().trim()

            if (properSearchQuery !== '' || properSearchQuery.length <= 0) {
                this.usersToView = this.usersCache.filter(el => {
                    for (let key in el) {
                        if (String(el[key]).toLowerCase().includes(properSearchQuery)) {
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
