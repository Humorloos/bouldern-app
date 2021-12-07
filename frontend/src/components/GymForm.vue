<template>
  <form action="/bouldern/add-gym/" method="post" enctype="multipart/form-data">
    <slot name="gym-form"></slot>
    <h3>Difficulty Levels</h3>
    <div id="difficulty-levels">
      <slot name="difficulty-levels"></slot>
      <difficulty-level-select
          v-for="difficultyLevelSelect in difficultyLevelSelects"
          :options="difficultyLevelSelect.options"
          :id="difficultyLevelSelect.id"
          :html-fields="difficultyLevelSelect.html"
          :key="difficultyLevelSelect.id"
      ></difficulty-level-select>
    </div>
    <button type="button" id="add-level-button" @click="addDifficultySelect">Add Level</button>
    <input type="submit" value="Submit">
  </form>
</template>

<script>
import DifficultyLevelSelect from "@/components/DifficultyLevelSelect";

export default {
  //Todo: check if GymForm is automatically matched to gym-form and name is unnecessary
  name: "gym-form",
  components: {
    DifficultyLevelSelect,
  },
  props: {
    initialDifficultyLevelSelects: Array,
  },
  data() {
    return {
      difficultyLevelSelects: this.initialDifficultyLevelSelects
    };
  },
  computed: {
    nextLevel() {
      return this.difficultyLevelSelects.length;
    }
  },
  methods: {
    addDifficultySelect() {
      const difficultyLevelSelect = {...this.difficultyLevelSelects[0]};
      difficultyLevelSelect.html = this.updateId(difficultyLevelSelect.html);
      difficultyLevelSelect.id = this.updateId(difficultyLevelSelect.id);
      this.difficultyLevelSelects.push(difficultyLevelSelect);
    },
    updateId(text) {
      return text.replaceAll("difficultylevel_set-0", 'difficultylevel_set-' + this.nextLevel);
    }
  }
}
</script>
