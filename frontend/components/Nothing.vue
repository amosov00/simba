<template lang="pug">
  div
    div.nothing-block
      div There is nothing here yet
</template>

<script>
export default {
  name: 'nothing',
}
</script>

<style lang="sass">
.nothing-block
  font-family: "Didact Gothic", "Roboto", sans-serif
  font-size: 22px
  color: #333333
  position: relative
  padding: 100px
  text-align: center
  &:after
    opacity: 0.05
    content: ""
    top: 0
    left: 0
    right: 0
    bottom: 0
    position: absolute
    z-index: -1
    background-image: url("~assets/images/SIMBA.svg")
    background-position: center
    background-repeat: no-repeat
    background-size: contain
</style>
