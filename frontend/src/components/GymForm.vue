<template>
  <v-row>
    <v-col>
      <v-text-field
        id="id_name"
        v-model="gymName"
        label="Name"
        type="text"
        :disabled="editing"
      />
    </v-col>
  </v-row>
  <v-row>
    <v-col>
      <v-img
        v-if="mapUrl !== ''"
        :src="mapUrl"
        max-height="300px"
        transition="false"
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
        :disabled="editing"
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
import {Colors} from '../constants/color';

export default {
  name: 'GymForm',
  components: {
    ColorSelect,
  },
  props: {
    editing: {
      type: Boolean,
      default: false,
    },
    initialData: {
      type: Object,
      default: () => {
        return {
          name: '',
          grade_set: [{'grade': 1, 'color': -1}],
        };
      },
    },
    initialMap: {
      type: Object,
      default: undefined,
    },
    initialExtraGradeId: {
      type: Number,
      default: null,
    },
    initialExtraColor: {
      type: Object,
      default: Colors.DEFAULT_COLOR,
    },
  },
  setup(props) {
    // gym
    const gymName = ref(props.initialData.name);
    const map = ref(props.initialMap ? [props.initialMap] : []);
    const mapUrl = computed(() => {
      if (map.value.length !== 0) return URL.createObjectURL(map.value[0]);
      else return '';
    });

    const store = useStore();

    // grades
    const regularGrades = props.initialData.grade_set
        .filter((grade) => grade.grade !== 'undefined');
    const gradeIds = ref(regularGrades.map((grade) => grade.id));
    const colors = ref(regularGrades
        .map((grade) => store.getters.colorById(grade.color)));

    const extraGrade = props.initialData.grade_set.find(
        (grade) => grade.grade === 'undefined');
    const extraGradeId = ref(extraGrade === undefined ?
        null : extraGrade.id);
    const extraColor = ref(extraGrade === undefined ?
        Colors.DEFAULT_COLOR : store.getters.colorById(extraGrade.color));
    const activeExtraColor = ref(extraGrade !== undefined);

    /**
     * Activates/deactivates the undefined grade color selector, on deactivation
     * also sets the selected color to the default value
     */
    function toggleExtraColor() {
      if (activeExtraColor.value) {
        extraColor.value = Colors.DEFAULT_COLOR;
      }
      activeExtraColor.value = !activeExtraColor.value;
    }

    /**
     * Adds the default color to colors to create new grade select
     */
    function addGradeSelect() {
      colors.value.push(Colors.DEFAULT_COLOR);
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
          grade: 'undefined',
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
        grade_set: grades.value,
      };
    });

    return {
      // gym properties
      gymName,
      map,
      mapUrl,
      // grade properties
      colors,
      extraColor,
      activeExtraColor,
      toggleExtraColor,
      addGradeSelect,
      removeGradeSelect,
      colorOptions: computed(() => store.state.colors),
      grades,
      gradeIds,
      // general properties
      form,
    };
  },
};
</script>

<style scoped>

</style>
