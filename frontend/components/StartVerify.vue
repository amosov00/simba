<template>
  <div>
<!--    <pre>{{res}}</pre>-->
    <step-indicator class="indicator"></step-indicator>
    <h2 class="start-title">Необходимо подтвердить вашу личность</h2>
    <p class="text">
      Если вы потеряете доступ к кошельку,<br />
      мы сможем идентифицировать вас по указанным данным.
    </p>
    <div class="lock">
      <img :src="require('@/static/lock.png')" alt="lock" class="lock__img" />
      <p class="lock__text">Безопасное соединение установлено, можно начинать проверку</p>
    </div>
    <btn-verify @click.native="$emit('show', false)">Начать проверку</btn-verify>
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
  data() {
    return {
      res: ''
    }
  },
  created() {
    this.$axios.get('/account/user/').then((res)=>{
      this.res = res.data
    })
  }
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
