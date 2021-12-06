<template>
  <v-select :options="options" :searchable="false" v-model="activeColor">
    <template #option="option">
      <span :style="option.style">{{ option.label }}</span>
    </template>
  </v-select>
</template>

<script>
import vSelect from "vue-select"

export default {
  name: "difficulty-level-select",
  components: {
    vSelect
  },
  props: {
    options: Object,
  },
  data() {
    return {activeColor: {label: "", style: {color: 'white'}}}
  },
}
</script>

<style>
.vs__selected::before {
  /*noinspection CssInvalidFunction*/
  background-color: v-bind("activeColor.style.color");
  border-radius: 50%;
  content: " ";
  display: flex;
  margin-right: 8px;
  height: 10px;
  width: 10px;
}
</style>