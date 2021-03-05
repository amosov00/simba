<template>
  <button
    :disabled="disabled"
    :class="{
      disabled,
    }"
  >
    <slot></slot>
  </button>
</template>

<script>
export default {
  name: 'BtnVerify',
  props: {
    disabled: {
      type: Boolean,
      default: false,
    },
  },
}
</script>

<style scoped>
button {
  width: 200px;
  height: 40px;
  background-color: #0060ff;
  color: white;
  border: 0 solid transparent;
  border-radius: 3px;
  font-weight: bold;
}
.disabled {
  background-color: #e5e5e5 !important;
  cursor: not-allowed;
}
</style>
