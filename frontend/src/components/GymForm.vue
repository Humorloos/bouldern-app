<template>
  <form
    action="/bouldern/add-gym/"
    method="post"
    enctype="multipart/form-data"
  >
    <slot name="gym-form" />
    <h3>Difficulty Levels</h3>
    <div id="difficulty-levels">
      <slot name="difficulty-levels" />
      <input
        id="id_difficultylevel_set-TOTAL_FORMS"
        type="hidden"
        name="difficultylevel_set-TOTAL_FORMS"
        :value="totalForms"
      >
      <difficulty-level-select
        v-for="difficultyLevelSelect in difficultyLevelSelects"
        :key="difficultyLevelSelect.prefix"
        :options="difficultyLevelSelect.options"
        :prefix="difficultyLevelSelect.prefix"
      >
        <div v-html="difficultyLevelSelect.html" />
      </difficulty-level-select>
    </div>
    <button
      id="add-level-button"
      type="button"
      @click="addDifficultySelect"
    >
      Add Level
    </button>
    <input
      type="submit"
      value="Submit"
    >
  </form>
</template>

<script>
import DifficultyLevelSelect from '@/components/DifficultyLevelSelect';

export default {
  name: 'GymForm',
  components: {
    DifficultyLevelSelect,
  },
  props: {
    initialDifficultyLevelSelects: {
      type: Array,
      default: function() {
        return [];
      },
    },
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
      difficultyLevelSelect.prefix = this
          .updateId(difficultyLevelSelect.prefix);
      this.difficultyLevelSelects.push(difficultyLevelSelect);
    },
    updateId(text) {
      return text.replaceAll(
          'difficultylevel_set-0', 'difficultylevel_set-' + this.totalForms);
    },
  },
};
</script>
