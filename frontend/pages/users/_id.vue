<template lang="pug">
  div.main-content
    div.is-size-4.mb-3
      span {{$t('account_page.account_info')}}
      =' — '
      strong {{ user_data.email.value }}
    ValidationObserver(ref="validation_obs" tag="div" v-slot="{ invalid }")
      div(v-for="(field, key) in user_data").is-flex.account-field
        div.account-field__label {{ $t(`account_page.${key}`) }}:
        div.flex-1
          div(v-if="field.type === 'string'")
            ValidationProvider(v-if="field.editable" v-slot="{ errors }" :rules="key === 'email' ? 'required|email' : 'required|alpha'")
              input(v-model="editable_data[key]" :name="$t(`account_page.${key}`)").account-field__input
              div(v-if="errors").validaton-error {{ errors[0] }}
            div(v-if="field['pre_hidden']") {{ field['pre_hidden'] }}
            div(v-else)
              span(v-if="!field.editable") {{ field.value }}
          div(v-else-if="field.type === 'array'")
            div(v-if="field.value.length === 0") {{ $t('account_page.list_is_empty') }}
            div(v-for="(el, i) in field.value" :key="i" style="height: 36px").is-flex.align-items-center
              div {{ el.address }}
              CopyToClipboard(:value_to_copy="el.address").ml-1
          div(v-else-if="field.type === 'addresses'")
            div(v-if="field.value.length === 0") {{ $t('account_page.list_is_empty') }}
            div(v-for="(el, i) in field.value.active" :key="i" style="height: 36px").is-flex.align-items-center
              div {{ el.address }}
              CopyToClipboard(:value_to_copy="el.address").ml-1
            div(v-if="field.value.archived.length > 0").mt-3
              div.deleted-addresses {{ $t('account_page.deleted_addresses') }}:
              div(v-for="(el, i) in field.value.archived" :key="i" style="height: 25px").is-flex.align-items-center
                div {{ timestampFromUtc(el.deleted_at) }} — {{ el.address }}
          div(v-else-if="field.type === 'date'") {{ timestampFromUtc(field.value) }}
          div(v-else-if="field.type === 'boolean'")
            div(v-if="field.editable" )
              b-switch(v-model="editable_data[key]")
            div(v-else) {{ field.value ? $t('account_page.yes') : $t('account_page.no') }}
          div(v-else) {{$t('account_page.not_available')}}
    div.has-text-centered.mt-4
      button(@click="save").btn {{$t('other.save')}}
</template>

<script>
import formatDate from "~/mixins/formatDate";
import CopyToClipboard from "~/components/CopyToClipboard";
import _ from 'lodash'

import { ValidationProvider } from 'vee-validate'

const editable = ['email', 'email_is_active', 'first_name',
  'last_name', 'is_active', 'is_staff', 'is_superuser', 'two_factor']

const pre_hidden = ['verification_code', 'recover_code', 'secret_2fa']

export default {
  name: "usersById",
  layout: "main",
  middleware: ["adminRequired"],
  mixins: [formatDate],

  components: {
    CopyToClipboard,
    ValidationProvider
  },

  created() {
    editable.forEach(el => {
      this.$set(this.editable_data, el, this.user_data[el].value)
    })

    this.editable_data_inital = JSON.parse(JSON.stringify(this.editable_data));
  },

  data: () => ({
    editable_data_inital: {},
    editable_data: {},
    disabled_save: true
  }),

  computed: {
    invoiceById() {
      return this.$store.getters['users/userById']
    }
  },


  watch: {
    editable_data: {
      handler: function(val, oldVal){
        if(JSON.stringify(val) !== JSON.stringify(this.editable_data_inital)) {
          this.disabled_save = false
        } else {
          this.disabled_save = true
        }
      }, deep: true
    }
  },

  methods: {
    report() {
      console.log(this.editable_data)
    },
    async save() {
      if(await this.$refs.validation_obs.validate()) {
        this.$axios.put(`/admin/users/${this.$nuxt.context.route.params.id}/`, this.editable_data).then(res => {
          if(res.data) {
            this.$buefy.toast.open({message: this.$i18n.t('account_page.account_changed_success'), type: 'is-primary'})
          } else {
            this.$buefy.toast.open({message: this.$i18n.t('account_page.account_changed_error'), type: 'is-danger'})
          }
        }).catch(() => {
          this.$buefy.toast.open({message: this.$i18n.t('account_page.account_changed_error'), type: 'is-danger'})
        })
      }
    }
  },

  async asyncData({store, route}) {

    let user_data = await store.dispatch("fetchUserById", route.params.id)

    let archived = await store.$axios.get(`/admin/users/${route.params.id}/archived_addresses/`)
      .then(res => res.data).catch(() => [])

    let addresses = {
      archived,
      active: {
        btc: [...user_data['user_btc_addresses']],
        eth: [...user_data['user_eth_addresses']]
      }
    }

    delete user_data['user_eth_addresses']
    delete user_data['user_btc_addresses']

    if(!_.isEmpty(user_data)) {
      for(const prop in user_data) {

        user_data[prop] = {
          value: user_data[prop],
          editable: false,
          pre_hidden: false,
          type: null
        }

        // Set type

        const value = user_data[prop]['value'];

        if(typeof value === 'string') {
          prop === 'created_at' ? user_data[prop]['type'] = 'date' : user_data[prop]['type'] = 'string'
        } else if(Array.isArray(value)) {
          user_data[prop]['type'] = 'array'
        } else if(typeof value === 'boolean') {
          user_data[prop]['type'] = 'boolean'
        }


        // Is editable
        if(editable.indexOf(prop) !== -1) {
          user_data[prop]['editable'] = true
        }

        // Pre-hide field
        if(pre_hidden.indexOf(prop) !== -1) {
          user_data[prop]['pre_hidden'] = true
        }
      }

      // set addresses active + archived
      // Archived addresses (deleted)
      if(archived.length > 0) {

        user_data['user_eth_addresses'] = {
          value: {
            active: addresses.active.eth,
            archived: []
          },
          editable: false,
          pre_hidden: false,
          type: 'addresses'
        }

        user_data['user_btc_addresses'] = {
          value: {
            active: addresses.active.btc,
            archived: []
          },
          editable: false,
          pre_hidden: false,
          type: 'addresses'
        }

        archived.forEach(el => {
          if(el.signature) {
            user_data['user_eth_addresses'].value.archived.push(el)
          } else {
            user_data['user_btc_addresses'].value.archived.push(el)
          }
        })
      }
    }

    return {
      user_data
    }
  }
};
</script>

<style lang="sass">
.deleted-addresses
  color: #bc6464

.account-field
  margin-left: -10px
  margin-right: -10px
  padding: 10px
  &__input
    border: 1px solid #cccccc
    border-radius: 2px
    width: 100%
    padding: 6px
  &__label
    width: 300px
    font-weight: bold
  &:nth-last-child(odd)
    background-color: #fcfcfc
</style>
