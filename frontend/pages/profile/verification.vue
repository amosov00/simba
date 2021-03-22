<template>
  <div>
    <div v-if="kycStatus !== ''">
      <step-indicator
        class="indicat"
        :emailConfirm="emailConfirm"
        :passportConfirm="documentReviewed"
        v-show="kycStatus === 'completed' || showStartVerify"
      >
      </step-indicator>
      <div id="sumsub-websdk-container" v-show="!showStartVerify"></div>
      <start-verify v-if="showStartVerify" @show="(e) => (showStartVerify = e)" :emailConfirm="emailConfirm">
      </start-verify>
    </div>
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


    await this.launch()
  },
  watch: {
    ['$i18n.locale']() {
      this.launch()
    }
  },
}
</script>
<style lang="scss">
.indicat {
  margin-left: 115px;
  margin-bottom: 30px;
}
</style>
