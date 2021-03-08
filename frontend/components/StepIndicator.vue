<template>
  <div class="wrap">
    <div class="step">
      <div
        class="step__number"
        :class="{
          'step__number--active': emailConfirm.is_active,
        }"
      >
        <p>1</p>
        <div
          class="step__line"
          :class="{
            'step__line--active': passportConfirm,
          }"
        ></div>
      </div>
      <p class="step__text">
        Подтверждение<br />
        email
      </p>
    </div>
    <div class="step">
      <div
        class="step__number"
        :class="{
          'step__number--active': passportConfirm,
        }"
      >
        <p>2</p>
      </div>
      <p class="step__text">
        Подтверждение<br />
        паспорта
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StepIndicator',
  props: {
    currentStep: {
      default: '',
      type: String,
    },
  },
  data() {
    return {
      emailConfirm: '',
      passportConfirm: ''
    }
  },
  created() {
    this.$axios.get('/account/kyc/status/')
      .then((res)=>{this.passportConfirm = res.data.kyc_current_status.docs_status.IDENTITY})
    this.$axios.get('/account/user/').then((res)=>{
      this.emailConfirm = res.data
      if (this.emailConfirm.kyc_review_response?.reviewResult?.reviewAnswer === 'RED') {
        this.emailConfirm.kyc_review_response = null
      }
    })
  }
}
</script>

<style scoped lang="scss">
.step__number--active ~ .step__text {
  color: #e0b72e;
}
.wrap {
  display: flex;
  justify-content: space-between;
  max-width: 500px;
  .step {
    position: relative;
    .step__number--active {
      background-color: #e0b72e !important;
    }
    .step__number {
      width: 30px;
      height: 30px;
      background-color: #c4c4c4;
      text-align: center;
      border-radius: 100%;
      vertical-align: middle;
      position: relative;
      margin-bottom: 8px;
      .step__line {
        position: absolute;
        width: 350px;
        height: 0;
        border-top: 2px dotted #c4c4c4;
        transform: translate(0, -50%);
        top: 50%;
        left: 37px;
      }
      .step__line--active {
        border-top: 2px dotted #e0b72e !important;
      }
      p {
        color: white;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-weight: bold;
        font-size: 17px;
      }
    }
  }
}
</style>
