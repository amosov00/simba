<template>
  <div class="wrap">
    <div class="step">
      <div class="step__number" :class="{
          'step__number--active': currentStep === 'first' ||
          currentStep === 'second' ||
          currentStep === 'third' ||
          currentStep === 'fourth'
        }"
      >
        <p>1</p>
        <div class="step__line" :class="{
          'step__line--active': currentStep === 'second' ||
          currentStep === 'third' ||
          currentStep === 'fourth'
        }"
        >
        </div>
      </div>
      <p class="step__text">Подтверждение<br> email</p>
    </div>
    <div class="step">
      <div class="step__number" :class="{
          'step__number--active': currentStep === 'second' ||
           currentStep === 'third' ||
           currentStep === 'fourth'
        }"
      >
        <p>2</p>
        <div class="step__line" :class="{
          'step__line--active': currentStep === 'third' || currentStep === 'fourth'
        }"
        >
        </div>
      </div>
      <p class="step__text">Подтверждение<br> паспорта</p>
    </div>
    <div class="step">
      <div class="step__number" :class="{
          'step__number--active': currentStep === 'third' || currentStep === 'fourth'
        }"
      >
        <p>3</p>
        <div class="step__line" :class="{
          'step__line--active': currentStep === 'fourth'
        }"
        >
        </div>
      </div>
      <p class="step__text">Подтверждение<br> адреса</p>
    </div>
    <div class="step">
      <div class="step__number" :class="{
          'step__number--active': currentStep === 'fourth'
        }"
      >
        <p>4</p>
      </div>
      <p class="step__text">Source of funds</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "StepIndicator",
  props: {
    currentStep: {
      default: '',
      type: String
    }
  }
}
</script>

<style scoped lang="scss">
.step__number--active ~ .step__text {
  color: #E0B72E;
}
.wrap {
  display: flex;
  justify-content: space-between;
  max-width: 500px;
  .step {
    position: relative;
    .step__number--active {
      background-color: #E0B72E !important;
    }
    .step__number {
      width: 30px;
      height: 30px;
      background-color: #C4C4C4;
      text-align: center;
      border-radius: 100%;
      vertical-align: middle;
      position: relative;
      margin-bottom: 8px;
      .step__line {
        position: absolute;
        width: 90px;
        height: 0;
        border-top: 2px dotted #C4C4C4;
        transform: translate(0, -50%);
        top: 50%;
        left: 37px;
      }
      .step__line--active {
        border-top: 2px dotted #E0B72E !important;
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
