<template lang="pug">
  ul.list
    slot
</template>

<script>
export default {};
</script>

<style lang="scss">
.list {
  width: 100%;
  border-radius: 0;
  box-shadow: none;

  &__item {
    width: 100%;
    padding: 6px 20px;
    background-color: #efefef;
    font-weight: 300;
    font-size: 18px;
    display: flex;
    justify-content: space-between;

    &:nth-child(1) {
      font-weight: bold;
    }

    &:nth-child(2n) {
      background-color: #fff;
      padding: 14px 20px;
    }

    &--name {
      text-align: left;
    }

    &--value {
      text-align: right;
    }

    .blue {
      color: #0060ff;
    }
  }
}
</style>
