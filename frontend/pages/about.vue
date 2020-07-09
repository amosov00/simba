<template lang="pug">
  div.main-content
    h1.is-size-4.has-text-weight-bold {{$t('header_menu.about')}}
    div.mt-4
      h3.is-size-5.has-text-weight-bold {{$t('about.company_goal')}}
      p.mt-1.main-content__text(v-html="$t('about.goal')")
    div.mt-4
      h3.is-size-5.has-text-weight-bold {{$t('about.date_of_establishment')}}
      p.mt-1.main-content__text {{$t('about.establishment')}}
    div.mt-4
      h3.is-size-5.has-text-weight-bold {{$t('about.сompany_locations')}}
      p.mt-1.main-content__text {{$t('about.locations')}}
    div.mt-4
      h3.is-size-5.has-text-weight-bold {{$t('about.our_mission')}}
      p.mt-1.main-content__text {{$t('about.mission')}}
</template>

<script>
  export default {
    name: "about",
    layout: "main",
    data() {
      return {
      };
    },
    methods: {
    },
  };
</script>

<style lang="sass" scoped>
</style>
