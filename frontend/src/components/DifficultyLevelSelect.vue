<template>
  <div id="difficulty_level">
    <div v-html="htmlFields"></div>
    <v-select :options="options" :searchable="false" v-model="activeColor" :id="id">
      <template #option="option">
        <span :style="option.style">{{ option.label }}</span>
      </template>
    </v-select>
  </div>
</template>

<script>
//TODO: fix / remove close button on right of select widget
import vSelect from "vue-select"

export default {
  name: "DifficultyLevelSelect",
  components: {
    vSelect
  },
  props: {
    options: Object,
    id: String,
    htmlFields: String,
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