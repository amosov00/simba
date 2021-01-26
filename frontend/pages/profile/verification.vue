<template lang="pug">
  div
    div#sumsub-websdk-container
</template>

<script>
import snsWebSdk from '@sumsub/websdk';
  export default {
    name: "profile-verification",
    layout: "profile",
    computed: {
    },
    data: () => ({
      steps: {
        current: 'profile.email_verification',
        list: ['profile.email_verification', 'profile.verify_address',
          'profile.id_verification', 'profile.source_of_funds_verification']
      }
    }),
    methods: {
    launchWebSdk(apiUrl, flowName, accessToken, applicantEmail, applicantPhone) {
        let snsWebSdkInstance = snsWebSdk.Builder(apiUrl, flowName)
            .withAccessToken(
                accessToken,
                (newAccessTokenCallback) => {
                    newAccessTokenCallback(accessToken)
                }
            )
            .withConf({
                lang: 'en',
                email: applicantEmail,
                phone: applicantPhone,
                onMessage: (type, payload) => {
                    console.log('WebSDK onMessage', type, payload)
                },
                onError: (error) => {
                    console.error('WebSDK onError', error)
                },
            })
            .build();
        snsWebSdkInstance.launch('#sumsub-websdk-container', 'basic-kyc')
    },
      activeStep(i) {
        if(this.failedStep(i)) {
          return false
        }
        return i < (this.steps.list.indexOf(this.steps.current)+1)
      },

      failedStep(i){
        if(this.stepFail) {
          if(i === this.stepFail) {
            return true
          }
        }

        return false
      }
    },
    async mounted() {
        let token = await this.$axios.get('/kyc/token')
        console.log(token);
        this.launchWebSdk('https://test-api.sumsub.com','basic-kyc', 'tst:Dt2mTU9SnHl9SGjALc5hhCMe.L4VJ9g2XHJbYjipw5hI39QZd7amHIzMo')
    },
    async asyncData({ store }) {
    }
  };
</script>

<style lang="sass" scoped></style>
