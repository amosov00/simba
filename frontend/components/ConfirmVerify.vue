<template>
  <div>
    <h2 class="start-title">Let's get you verified</h2>
    <p class="text">Before you start, please prepare your identity document and make sure it is valid. We also require you to accept our T’s&C’s, and to agree to our processing of your personal data:</p>
    <check-box-verify @change="e => firstCheck = e">By clicking Next, I accept <a href="#">the Terms and Conditions</a></check-box-verify>
    <check-box-verify @change="e => secondCheck = e">I agree to the processing of my personal dara, as described in <br> <a href="#">the Consent to Personal Data Processing</a></check-box-verify>
    <btn-verify
      :disabled="!firstCheck || !secondCheck"
      class="btn"
    >Next</btn-verify>
  </div>
</template>

<script>
import BtnVerify from '@/components/BtnVerify'
import CheckBoxVerify from '@/components/CheckBoxVerify'
export default {
name: "ConfirmVerify",
  components: { CheckBoxVerify, BtnVerify },
  data() {
    return {
      firstCheck: false,
      secondCheck: false
    }
  }
}
</script>

<style scoped lang="scss">
.start-title {
  font-size: 18px;
  font-weight: bold;
}
.text {
  font-size: 18px;
  margin-top: 10px;
  margin-bottom: 47px;
}
a {
  text-decoration: underline;
}
.btn {
  margin-top: 40px;
}
</style>
