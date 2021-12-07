<template>
  <form action="/bouldern/add-gym/" method="post" enctype="multipart/form-data">
    <slot name="gym-form"></slot>
    <h3>Difficulty Levels</h3>
    <div id="difficulty-levels">
      <slot name="difficulty-levels"></slot>
      <input
          type="hidden"
          name="difficultylevel_set-TOTAL_FORMS"
          id="id_difficultylevel_set-TOTAL_FORMS"
          :value="totalForms"
      >
      <difficulty-level-select
          v-for="difficultyLevelSelect in difficultyLevelSelects"
          :options="difficultyLevelSelect.options"
          :prefix="difficultyLevelSelect.prefix"
          :key="difficultyLevelSelect.prefix"
      ><div v-html="difficultyLevelSelect.html"></div></difficulty-level-select>
    </div>
    <button type="button" id="add-level-button" @click="addDifficultySelect">Add Level</button>
    <input type="submit" value="Submit">
  </form>
</template>

<script>
import DifficultyLevelSelect from "@/components/DifficultyLevelSelect";

export default {
  name: "GymForm",
  components: {
    DifficultyLevelSelect,
  },
  props: {
    initialDifficultyLevelSelects: Array,
  },
  data() {
    return {
      difficultyLevelSelects: this.initialDifficultyLevelSelects,
    };
  },
  computed: {
    totalForms() {
      return this.difficultyLevelSelects.length;
    },
  },
  methods: {
    addDifficultySelect() {
      const difficultyLevelSelect = {...this.difficultyLevelSelects[0]};
      difficultyLevelSelect.html = this.updateId(difficultyLevelSelect.html)
          .replace('value="0"', `value="${this.totalForms}"`);
      difficultyLevelSelect.prefix = this.updateId(difficultyLevelSelect.prefix)
      this.difficultyLevelSelects.push(difficultyLevelSelect);
    },
    updateId(text) {
      return text.replaceAll("difficultylevel_set-0", 'difficultylevel_set-' + this.totalForms);
    }
  }
}
</script>
