<template>
  <div>
<!--    <step-indicator-->
<!--      class="indicator"-->
<!--      :emailConfirm="emailConfirm"-->
<!--    >-->
<!--    </step-indicator>-->
    <h2 class="start-title">{{$t('verify["You need to verify your identity"]')}}</h2>
    <p class="text">
      {{$t('verify["If you lose access to your wallet"]')}},<br />
      {{$t('verify["we will be able to identify you by the specified data"]')}}.
    </p>
    <div class="lock">
      <img :src="require('@/static/lock.png')" alt="lock" class="lock__img" />
      <p class="lock__text">{{$t('verify["A secure connection has been established, you can start testing"]')}}</p>
    </div>
    <btn-verify @click.native="$emit('show', false)">{{$t('verify["To be tested"]')}}</btn-verify>
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
  props: {
    emailConfirm: {
      default: false,
      type: Boolean
    }
  },
}
</script>

<style scoped lang="scss">
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
