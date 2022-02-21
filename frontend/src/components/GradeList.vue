<template>
  <v-row>
    <v-col class="text-subtitle-1">
      Grades
    </v-col>
    <v-col>
      <v-btn
        id="add-grade-button"
        type="button"
        @click="addGradeSelect"
      >
        Add Grade
      </v-btn>
    </v-col>
    <v-col>
      <v-btn
        to="/create-color"
      >
        New Color
      </v-btn>
    </v-col>
  </v-row>
  <v-row
    v-for="(color, index) in colors"
    :key="color.name"
  >
    <v-col
      align-self="center"
      class="flex-grow-0"
    >
      {{ index + 1 }}.
    </v-col>
    <v-col align-self="center">
      <color-select
        :id="`id_color-grade-${index + 1}`"
        v-model="colors[index]"
        :color-options="colorOptions"
      />
    </v-col>
    <v-col
      align-self="center"
      class="flex-grow-0"
    >
      <v-btn
        icon="mdi-close"
        flat
        size="small"
        @click="removeGradeSelect(index)"
      />
    </v-col>
  </v-row>
  <v-row>
    <v-col
      class="flex-grow-0"
      align-self="center"
    >
      <v-checkbox
        id="id_undefined_grade_active"
        hide-details
        label="Use undefined grade?"
        @click="toggleExtraColor"
      />
    </v-col>
    <v-col align-self="center">
      <color-select
        id="id_color-undefined"
        v-model="extraColor"
        :disabled="!activeExtraColor"
        :color-options="colorOptions"
      />
    </v-col>
  </v-row>
</template>
<script>
/** @file todo */

import {computed, ref} from 'vue';
import ColorSelect from './ColorSelect.vue';
import {useStore} from 'vuex';
const defaultColor = {
  color: 'white',
  name: '',
  id: 0,
};

export default {
  name: 'GradeList',
  components: {
    ColorSelect,
  },
  props: {
    colorOptions: {
      type: Array,
      default: () => [],
    },
  },
  setup() {
    const defaultColor = {
      color: 'white',
      name: '',
      id: 0,
    };
    const colors = ref([defaultColor]);
    const extraColor = ref(defaultColor);
    const activeExtraColor = ref(false);

    /**
     * Activates/deactivates the undefined grade color selector, on deactivation
     * also sets the selected color to the default value
     */
    function toggleExtraColor() {
      if (activeExtraColor.value) {
        extraColor.value = defaultColor;
      }
      activeExtraColor.value = !activeExtraColor.value;
    }
    /**
     * Adds the default color to colors to create new grade select
     */
    function addGradeSelect() {
      colors.value.push(defaultColor);
    }
    /**
     * Removes the color with provided index from colors to remove the
     * corresponding grade select
     */
    function removeGradeSelect(index) {
      colors.value.splice(index, 1);
    }

    const store = useStore();

    return {
      defaultColor,
      colors,
      extraColor,
      activeExtraColor,
      toggleExtraColor,
      addGradeSelect,
      removeGradeSelect,
      colorOptions: computed(() => store.state.colors),
    };
  },
};
</script>

<style scoped>

</style>
