<template>
  <div>
    <div v-if="kyc_status !== ''">
      <step-indicator
        class="indicat"
        :emailConfirm="emailConfirm"
        :passportConfirm="documentReviewed"
        v-if="kyc_status === 'completed'"
      >
      </step-indicator>
      <div id="sumsub-websdk-container" v-show="!showStartVerify"></div>
      <start-verify
        v-if="showStartVerify"
        @show="e => showStartVerify = e"
        :emailConfirm="emailConfirm"
      >
      </start-verify>
    </div>
    <pre v-show="false">{{language}}</pre>
  </div>
</template>

<script>
import snsWebSdk from '@sumsub/websdk'
import StartVerify from '@/components/StartVerify'
import StepIndicator from '@/components/StepIndicator'
export default {
  name: 'profile-verification',
  layout: 'profile',
  computed: {
    language() {
      const lang = this.$i18n.locale
      this.launch()
      return lang
    },
    documentReviewed() {
      return this.reviewAnswer === 'GREEN' && this.reviewStatus === 'completed'
    },
    flow() {
      if (this.$i18n.locale === 'ru') {
        return 'Basic_ru'
      } else {
        return 'basic-kyc'
      }
    }
  },
  components: {
    StartVerify,
    StepIndicator
  },
  data: () => ({
    token: null,
    currentStep: '',
    stepsCompleted: [],
    stepsNext: [],
    showStartVerify: true,
    emailConfirm: false,
    kyc_status: '',
    reviewAnswer: '',
    reviewStatus: ''
  }),
  methods: {
    async launch() {
      let { data } = await this.$axios.get('/account/kyc/token/')
      this.token = data.token
      // 'tst:Dt2mTU9SnHl9SGjALc5hhCMe.L4VJ9g2XHJbYjipw5hI39QZd7amHIzMo'
      this.launchWebSdk('https://test-api.sumsub.com', this.flow, this.token)
    },
    launchWebSdk(apiUrl, flowName, accessToken, applicantEmail, applicantPhone) {
      const origin = document.location.origin
      let snsWebSdkInstance = snsWebSdk
        .Builder(apiUrl, flowName)
        .withAccessToken(accessToken, (newAccessTokenCallback) => {
          newAccessTokenCallback(accessToken)
        })
        .withConf({
          lang: this.$i18n.locale,
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
            customCss: `${origin}/${this.$i18n.locale}sumsub.css`,
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
    await this.launch()
  },
  created() {
    this.$axios.get('/account/user/').then((res)=>{
      this.emailConfirm = res.data.is_active
      this.kyc_status = res.data.kyc_status
      this.reviewStatus = res.data.kyc_review_response.reviewStatus
      this.reviewAnswer = res.data.kyc_review_response.reviewResult.reviewAnswer
      if (this.kyc_status === 'completed') {
        this.showStartVerify = false
      }
    })
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
<style lang="scss">
  .indicat {
    margin-left: 135px;
    margin-bottom: 30px;
  }
</style>
