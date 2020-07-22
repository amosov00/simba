<template lang="pug">
  div.main-content
    h1.title.is-size-4 Account information
    div(v-for="(field, key) in user_data").is-flex.account-field
      div.account-field__label {{ $t(`account_page.${key}`) }}:
      div.flex-1
        div(v-if="field.type === 'string'")
          input(v-if="field.editable" :value="field.value").w-100.input
          div(v-if="field['pre_hidden']") Hidden {{ field['pre_hidden'] }}
          div(v-else)
            span(v-if="!field.editable") Value: {{ field.value }}
        div(v-else-if="field.type === 'array'")
          div(v-for="(el, i) in field.value" :key="i" style="height: 36px").is-flex.align-items-center
            div {{ el.address }}
            CopyToClipboard(:value_to_copy="el.address").ml-1
        div(v-else-if="field.type === 'date'") {{ timestampFromUtc(field.value) }}
        div(v-else-if="field.type === 'boolean'")
          div(v-if="field.editable" )
            b-switch(:value="field.value")
          div(v-else) {{ field.value ? 'Yes' : 'No' }}
        div(v-else) N/A

</template>

<script>
import formatDate from "~/mixins/formatDate";
import formatCurrency from "~/mixins/formatCurrency";


import CopyToClipboard from "~/components/CopyToClipboard";

import _ from 'lodash'

const editable = ['email', 'email_is_active', 'first_name',
  'last_name', 'is_active', 'is_manager', 'is_superuser', 'two_factor']

const pre_hidden = ['verification_code', 'recover_code', 'secret_2fa']

export default {
  name: "usersById",
  layout: "main",
  middleware: ["adminRequired"],
  mixins: [formatDate, formatCurrency],

  components: {
    CopyToClipboard
  },

  computed: {
    invoiceById() {
      return this.$store.getters['users/userById']
    }
  },
  async asyncData({store, route}) {

    let user_data = await store.dispatch("fetchUserById", route.params.id)

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
          console.log(user_data[prop])
        }
      }
    }

    return {
      user_data
    }
  }
};
</script>

<style lang="sass">
.account-field
  padding: 10px

  &__label
    width: 300px
    font-weight: bold
  &:nth-last-child(odd)
    background-color: #fcfcfc
</style>
