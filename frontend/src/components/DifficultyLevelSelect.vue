<template>
  <div id="difficulty-level">
    <slot></slot>
    <input
        type="hidden"
        :name="colorFieldName"
        :id="colorFieldId"
        :value="activeColor.value"
    >
    <v-select :options="options" :searchable="false" :clearable="false" v-model="activeColor">
      <template #option="option">
        <span :style="option.style">{{ option.label }}</span>
      </template>
    </v-select>
  </div>
</template>

<script>
import vSelect from "vue-select"

export default {
  name: "DifficultyLevelSelect",
  components: {
    vSelect
  },
  props: {
    options: Object,
    prefix: String,
  },
  data() {
    return {
      activeColor: {
        label: "",
        style: {color: 'white'},
        value: -1,
      }
    }
  },
  computed: {
    colorFieldName() {
      return this.prefix + "-color"
    },
    colorFieldId() {
      return "id_" + this.colorFieldName
    },
  }
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