<template>
  <div>
    <div v-if="kycStatus !== ''">
      <step-indicator
        class="indicat"
        :emailConfirm="emailConfirm"
        :passportConfirm="documentReviewed"
        v-if="kycStatus === 'completed'"
      >
      </step-indicator>
      <div id="sumsub-websdk-container" v-show="!showStartVerify"></div>
      <start-verify v-if="showStartVerify" @show="(e) => (showStartVerify = e)" :emailConfirm="emailConfirm">
      </start-verify>
    </div>
    <pre v-show="false">{{ language }}</pre>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'
import snsWebSdk from '@sumsub/websdk'
import StartVerify from '@/components/StartVerify'
import StepIndicator from '@/components/StepIndicator'

export default {
  name: 'profile-verification',
  layout: 'profile',
  computed: {
    ...mapState(['user', 'kyc']),
    language() {
      const lang = this.$i18n.locale
      this.launch()
      return lang
    },
    emailConfirm() {
      return this.user.is_active
    },
    documentReviewed() {
      return this.kyc.is_verified && this.kyc.status === 'completed'
    },
    kycStatus() {
      return this.kyc ? this.kyc.status : ''
    },
    flow() {
      if (this.$i18n.locale === 'ru') {
        return 'Basic_ru'
      } else {
        return 'basic-kyc'
      }
    },
  },
  components: {
    StartVerify,
    StepIndicator,
  },
  data: () => ({
    stepsCompleted: [],
    stepsNext: [],
    showStartVerify: true,
  }),
  methods: {
    ...mapActions(['getKYCStatus', 'getKYCToken']),
    async launch() {
      this.launchWebSdk(this.$config.sumsubURL, this.flow, await this.getKYCToken())
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
    if (_.isEmpty(this.kyc)) {
      await this.getKYCStatus()
    }

    this.showStartVerify = !this.kyc.is_verified

    if (localStorage.getItem('currentStep')) {
      this.currentStep = localStorage.getItem('currentStep')
    }

    await this.launch()
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
