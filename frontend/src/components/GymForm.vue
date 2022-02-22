<template>
  <v-row>
    <v-col>
      <v-text-field
        id="id_name"
        v-model="gymName"
        label="Name"
        type="text"
        :disabled="edit"
      />
    </v-col>
  </v-row>
  <v-row>
    <v-col align-self="center">
      <v-file-input
        id="id_map"
        v-model="map"
        accept="image/*"
        label="Map"
        :disabled="edit"
      />
    </v-col>
    <v-col>
      <v-img
        v-if="mapUrl !== ''"
        :src="mapUrl"
        transition="false"
      />
    </v-col>
  </v-row>
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
        v-model="activeExtraColor"
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
  name: 'GymForm',
  components: {
    ColorSelect,
  },
  props: {
    edit: {
      type: Boolean,
      default: false,
    },
    initialGymName: {
      type: String,
      default: '',
    },
    initialGradeIds: {
      type: Array,
      default: () => [0],
    },
    initialColors: {
      type: Array,
      default: () => [defaultColor],
    },
    initialExtraGradeId: {
      type: Number,
      default: null,
    },
    initialExtraColor: {
      type: Object,
      default: defaultColor,
    },
    initiallyActiveExtraColor: {
      type: Boolean,
      default: false,
    },
  },
  setup(props) {
    // gym
    const gymName = ref(props.initialGymName);
    const map = ref([]);
    const mapUrl = computed(() => {
      if (map.value.length !== 0) return URL.createObjectURL(map.value[0]);
      else return '';
    });

    // grades
    const gradeIds = ref(props.initialGradeIds);
    const colors = ref(props.initialColors);
    const extraGradeId = ref(props.initialExtraGradeId);
    const extraColor = ref(props.initialExtraColor);
    const activeExtraColor = ref(props.initiallyActiveExtraColor);

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
      if (gradeIds[index] !== undefined) {
        gradeIds.value.splice(index, 1);
      }
    }

    const store = useStore();

    const grades = computed(() => {
      const grades = colors.value.map((color, index) => {
        const grade = {
          color: color.id,
          grade: index + 1,
        };
        if (gradeIds.value[index] !== undefined) {
          grade.id = gradeIds.value[index];
        }
        return grade;
      });
      if (activeExtraColor.value) {
        const extraGrade = {
          color: extraColor.value.id,
          grade: NaN,
        };
        if (extraGradeId.value !== null) extraGrade.id = extraGradeId.value;
        grades.push(extraGrade);
      }
      return grades;
    });

    /**
     * Gets a form with the gym's name and all grades for creation
     *
     * @returns {object} the gym form
     */
    const form = computed(() => {
      return {
        name: gymName.value,
        grade_set: grades,
      };
    });

    return {
      // gym properties
      gymName,
      map,
      mapUrl,
      // grade properties
      defaultColor,
      colors,
      extraColor,
      activeExtraColor,
      toggleExtraColor,
      addGradeSelect,
      removeGradeSelect,
      colorOptions: computed(() => store.state.colors),
      grades,
      // general properties
      form,
    };
  },
};
</script>

<style scoped>

</style>
