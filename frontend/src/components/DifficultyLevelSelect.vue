<template>
  <v-select :options="options" :searchable="false">
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
  // computed: {
  //   options() {
  //     console.log("asdf")
  //     return ""
  //   }
  // }
}
</script>

<style scoped>

</style>