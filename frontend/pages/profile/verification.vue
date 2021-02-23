<template>
  <div>
    <div id="sumsub-websdk-container"></div>
    <div>{{currentStep}}</div>
  </div>
</template>

<script>
import snsWebSdk from '@sumsub/websdk'
import { sumSubStyles } from '~/consts'
export default {
  name: 'profile-verification',
  layout: 'profile',
  computed: {},
  data: () => ({
    token: null,
    currentStep: ''
  }),
  methods: {
    launchWebSdk(apiUrl, flowName, accessToken, applicantEmail, applicantPhone) {
      let snsWebSdkInstance = snsWebSdk
        .Builder(apiUrl, flowName)
        .withAccessToken(accessToken, (newAccessTokenCallback) => {
          newAccessTokenCallback(accessToken)
        })
        .withConf({
          lang: 'en',
          email: applicantEmail,
          phone: applicantPhone,
          onMessage: (type, payload) => {
            console.log('WebSDK onMessage', type, payload)
            if (type === 'idCheck.onStepInitiated') {
              this.currentStep = payload.idDocSetType
            }
          },
          uiConf: {
            customCssStr: sumSubStyles
          },
          onError: (error) => {
            console.error('WebSDK onError', error)
          },
        })
        .build()
      snsWebSdkInstance.launch('#sumsub-websdk-container', 'basic-kyc')
    },
  },
  async mounted() {
    let { data } = await this.$axios.get('/account/kyc/token/')
    this.token = data.token
    // 'tst:Dt2mTU9SnHl9SGjALc5hhCMe.L4VJ9g2XHJbYjipw5hI39QZd7amHIzMo'
    this.launchWebSdk('https://test-api.sumsub.com', 'basic-kyc', this.token)
  },
}
</script>
