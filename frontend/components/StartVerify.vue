<template>
  <div>
    <h2 class="start-title">{{ $t('verify["You need to verify your identity"]') }}</h2>
    <ul class="text">
      <li class="mb-3 mt-3">{{ $t('verify.oneItem') }}</li>
      <li>{{ $t('verify.twoItem') }}</li>
    </ul>
    <div class="lock">
      <img :src="require('@/static/lock.png')" alt="lock" class="lock__img" />
      <p class="lock__text">{{ $t('verify["A secure connection has been established, you can start testing"]') }}</p>
    </div>
    <btn-verify @click.native="$emit('show', false)">{{ $t('verify["To be tested"]') }}</btn-verify>
  </div>
</template>

<script>
import BtnVerify from '@/components/BtnVerify'
import StepIndicator from '@/components/StepIndicator'
export default {
  name: 'StartVerify',
  components: {
    BtnVerify,
    StepIndicator,
  },
}
</script>

<style scoped lang="scss">
ul {
  list-style-type: disc;
  list-style-position: inside;
  li {
    font-weight: 300;
  }
}
.indicator {
  margin-bottom: 72px;
}
.start-title {
  font-size: 18px;
  font-weight: bold;
}
.text {
  font-size: 18px;
  margin-top: 10px;
  margin-bottom: 47px;
}
.lock {
  display: flex;
  margin-bottom: 32px;
  .lock__text {
    color: #8b8b8b;
    margin-left: 9px;
    text-align: center;
  }
}
</style>
