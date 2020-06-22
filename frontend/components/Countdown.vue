<template lang="pug">
  div.countdown__digits(:class="{'countdown__digits--red': done}")
    VueCountdown(:time="countdownTime" @end="onEnd")
      template(slot-scope="props")
        | {{ twoDigits(props.hours) }}:{{ twoDigits(props.minutes) }}:{{ twoDigits(props.seconds) }}
</template>

<script>
  import VueCountdown from '@chenfengyuan/vue-countdown';

  import moment from 'moment';

  export default {
    name: 'countdown',
    components: {VueCountdown},
    props: {
      date: String,
    },

    data: () => ({
      countdownTime: 100000,
      done: false
    }),

    mounted() {
      this.countdownTime = this.dt();
    },

    methods: {
      dt() {
        let current = +Date.now();
        let dt = +moment.utc(this.date).toDate();

        let plus2hours = +dt + (2*60*60*1000)


        let diff = plus2hours - current;

        if(diff < 0) {
          return 0
        }

        return diff
      },

      onEnd() {
        console.log('timer done!');
        this.done = true;
      },

      twoDigits(number) {
        if(number.toString().length < 2){
          return "0" + number
        }
        return number
      }
    }
  }
</script>

<style lang="sass">
  .countdown
    &__digits
      font-style: normal
      font-weight: 300
      font-size: 36px
      line-height: 100%
      color: #000000
      &--red
        color: #DC6161
</style>
