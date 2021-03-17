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
     KYCtoken() {
      return this.$store.getters['sumsub/KYCtoken']
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
      await this.$store.dispatch('sumsub/fetchKYCtoken')
      this.launchWebSdk('https://test-api.sumsub.com', this.flow, this.KYCtoken)
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
  async created() {
    const res = await this.$store.dispatch('sumsub/fetchUserData')
    this.emailConfirm = res.data.is_active
    this.kyc_status = res.data.kyc_status
    this.reviewStatus = res.data.kyc_review_response.reviewStatus
    this.reviewAnswer = res.data.kyc_review_response.reviewResult.reviewAnswer
    if (this.kyc_status === 'completed') {
      this.showStartVerify = false
    }
    await this.launch()
  },
}
</script>
<style lang="scss">
  .indicat {
    margin-left: 135px;
    margin-bottom: 30px;
  }
</style>
