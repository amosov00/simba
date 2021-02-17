<template lang="pug">
  div.modal-card(style="max-width: 400px")
    section.modal-card-body.text-center
      div(class="modal-card-title").text-center Amount: {{ amount }}
      qrcode-vue(:value="qrcode_value" :size="200" level="H").mt-4
</template>

<script>
import QrcodeVue from 'qrcode.vue'

export default {
  name: 'AddressQRCode',
  components: { QrcodeVue },
  props: {
    qrcode_value: String,
    amount: null,
  },
  data: () => ({}),
  methods: {},
}
</script>

<style lang="sass" scoped>
.modal-card-body
  padding-top: 40px
  padding-bottom: 40px
</style>
