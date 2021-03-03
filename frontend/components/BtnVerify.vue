<template>
  <button :disabled="disabled" :class="{
    disabled
  }">
    <slot></slot>
  </button>
</template>

<script>
export default {
  name: "BtnVerify",
  props: {
    disabled: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style scoped>
  button {
    width: 200px;
    height: 40px;
    background-color: #0060FF;
    color: white;
    border: 0 solid transparent;
    border-radius: 3px;
    font-weight: bold;
  }
  .disabled {
    background-color: #E5E5E5 !important;
    cursor: not-allowed;
  }
</style>
