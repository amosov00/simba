<template lang="pug">
  div
    div.main-content
      div
        h1.title.is-size-4 {{$t('about.company_goal')}}
        p.subtitle(v-html="$t('about.goal')")
      div.mt-4
        h1.title.is-size-4 {{$t('about.date_of_establishment')}}
        p.subtitle {{$t('about.establishment')}}
      div.mt-4
        h1.title.is-size-4 {{$t('about.сompany_locations')}}
        p.subtitle {{$t('about.locations')}}
      div.mt-4
        h1.title.is-size-4 {{$t('about.our_mission')}}
        p.subtitle {{$t('about.mission')}}
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
