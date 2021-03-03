<template>
  <div class="wrap">
    <div class="checkbox">
      <input type="checkbox" :id="label" @change="$emit('change', $event.target.checked)">
      <label :for="label"></label>
    </div>
    <p class="description"><slot></slot></p>
  </div>
</template>

<script>
export default {
  name: "CheckBoxVerify",
  data() {
    return {
      label: '',
    }
  },
  created() {
    this.label = `label${Math.random()}`
  }
}
</script>

<style scoped lang="scss">
 input {
    display: none;
 }
 .checkbox {
   margin-right: 20px;
 }

 label {
   display: block;
   width: 18px;
   height: 18px;
   outline: 1px solid #DFDFDF;
 }
.wrap {
  display: flex;
  margin-top: 10px;
}
 input:checked ~ label {
   position: relative;
   outline: 2px solid #0060FF;
   outline-offset: -2px;
 }

 input:checked ~ label::before {
   content: '';
   display: block;
   width: 10px;
   height: 10px;
   position: absolute;
   transform: translate(-50%, -50%);
   top: 50%;
   left: 50%;
   background-color: #0060FF;
 }
</style>
