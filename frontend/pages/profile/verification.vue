<template lang="pug">
  div
    div.steps.is-flex.align-items-center
      div(v-for="(step, i) in steps.list" :key="i" :class="{ 'steps-item--failed': failedStep(i), 'steps-item--active': activeStep(i)}").steps-item.steps-item--profile
        | {{ i+1 }}
        div.steps-item__text {{ step }}
</template>

<script>

  export default {
    name: "profile-verification",
    layout: "profile",
    computed: {
    },
    data: () => ({
      steps: {
        current: 'Email verification',
        list: ['Email verification', 'Verify address', 'ID verification', 'Source of funds verification']
      }
    }),
    methods: {
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
    created() {
    },
    async asyncData({ store }) {
    }
  };
</script>

<style lang="sass" scoped></style>
