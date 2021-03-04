<template>
  <div>
    <div id="sumsub-websdk-container"></div>
    <start-verify v-if="false"></start-verify>
  </div>
</template>

<script>
import snsWebSdk from '@sumsub/websdk'
import StartVerify from '@/components/StartVerify'
export default {
  name: 'profile-verification',
  layout: 'profile',
  computed: {},
  components: {
    StartVerify,
  },
  data: () => ({
    token: null,
    currentStep: '',
    stepsCompleted: [],
    stepsNext: [],
  }),
  methods: {
    launchWebSdk(apiUrl, flowName, accessToken, applicantEmail, applicantPhone) {
      const origin = document.location.origin
      console.log(`${origin}/sumsub.css`)
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
              localStorage.setItem('currentStep', payload.idDocSetType)
            }
            if (type === 'livenessSessionCompleted' && payload.answer === 'GREEN') {
              this.currentStep = 'APPLICANT_DATA'
              localStorage.setItem('currentStep', 'APPLICANT_DATA')
            }
          },
          uiConf: {
            customCss: `${origin}/sumsub.css`,
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
  created() {
    if (localStorage.getItem('currentStep')) {
      this.currentStep = localStorage.getItem('currentStep')
    }
  },
  watch: {
    currentStep() {
      if (this.currentStep === 'IDENTITY') {
        this.stepsCompleted = []
        this.stepsNext = ['SELFIE', 'APPLICANT_DATA']
      }
      if (this.currentStep === 'SELFIE') {
        this.stepsCompleted = ['IDENTITY']
        this.stepsNext = ['APPLICANT_DATA']
      }
      if (this.currentStep === 'APPLICANT_DATA') {
        this.stepsCompleted = ['IDENTITY', 'SELFIE']
        this.stepsNext = []
      }
    },
  },
}
</script>
