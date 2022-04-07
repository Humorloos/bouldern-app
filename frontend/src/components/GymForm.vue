<template>
  <v-form
    ref="form"
    lazy-validation
  >
    <v-row>
      <v-col>
        <v-text-field
          id="id_name"
          v-model="gymName"
          :label="$t('gymForm.lblName')"
          type="text"
          :disabled="editing"
          :rules="[requiredRule($t('gymForm.lblName'))]"
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
          :label="$t('gymForm.lblMap')"
          :disabled="editing"
          :rules="[requiredImageRule]"
          :hint="$t('gymForm.createMapHint', {link: mapHintLinkElement})"
          persistent-hint
        >
          <template #message="{ message }">
            <span v-html="message" />
          </template>
        </v-file-input>
      </v-col>
    </v-row>
    <v-row>
      <v-col class="text-subtitle-1">
        {{ $t('grades') }}
      </v-col>
      <v-col>
        <v-btn
          id="add-grade-button"
          type="button"
          @click="addGradeSelect"
        >
          {{ $t('gymForm.lblAddGrade') }}
        </v-btn>
      </v-col>
      <v-col>
        <v-btn
          to="/create-color"
        >
          {{ $t('gymForm.lblNewColor') }}
        </v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-input
          v-model="regularGradeColors"
          :rules="[atLeastOneGradeRule]"
        >
          <v-container>
            <v-row
              v-for="(color, index) in regularGradeColors"
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
                  v-model="regularGradeColors[index]"
                  :color-options="colorOptions"
                />
              </v-col>
              <v-col
                align-self="center"
                class="flex-grow-0"
              >
                <v-btn
                  :id="`id_remove-grade-${index + 1}`"
                  icon="mdi-close"
                  flat
                  size="small"
                  @click="removeGradeSelect(index)"
                />
              </v-col>
            </v-row>
          </v-container>
        </v-input>
      </v-col>
    </v-row>
    <v-row>
      <v-col
        class="flex-grow-0"
        align-self="center"
      >
        <v-checkbox
          id="id_undefined-grade-active"
          v-model="activeExtraColor"
          hide-details
          :label="$t('gymForm.lblUseUndefinedGrade')"
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
    <v-row>
      <v-col>
        <v-btn
          id="id_save-gym"
          @click="validateForm"
        >
          {{ $t('gymForm.lblSave') }}
        </v-btn>
      </v-col>
    </v-row>
  </v-form>
</template>
<script>
/** @file form for creating or editing Gyms */

import {computed, ref} from 'vue';
import ColorSelect from './ColorSelect.vue';
import {useStore} from 'vuex';
import {Colors} from '../constants/color';
import {
  atLeastOneGradeRule,
  requiredImageRule,
  requiredRule,
} from '../helpers/rules.js';
import {useI18n} from 'vue-i18n';

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
          map: '',
          grade_set: [{'grade': 1, 'color': -1}],
        };
      },
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
  emits: ['save'],
  setup(props, {emit}) {
    // form
    const form = ref(null);

    /**
     * Validates the form and emits save signal if form is valid
     */
    function validateForm() {
      form.value.validate().then((result) => {
        if (result.valid) {
          emit('save');
        }
      });
    }

    // gym
    const gymName = ref(props.initialData.name);
    const map = ref([new File([], props.initialData.map.split('/').at(-1))]);
    const mapUrl = computed(() => {
      if (map.value.length > 0 && map.value[0].size !== 0) {
        return URL.createObjectURL(map.value[0]);
      } else {
        return props.initialData.map;
      }
    });

    const store = useStore();

    // grades
    const regularGrades = props.initialData.grade_set
        .filter((grade) => grade.grade !== 'undefined');
    const gradeIds = ref(regularGrades.map((grade) => grade.id));
    const regularGradeColors = ref(regularGrades
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
      regularGradeColors.value.push(Colors.DEFAULT_COLOR);
    }

    /**
     * Removes the color with provided index from colors to remove the
     * corresponding grade select
     */
    function removeGradeSelect(index) {
      regularGradeColors.value.splice(index, 1);
      if (gradeIds[index] !== undefined) {
        gradeIds.value.splice(index, 1);
      }
    }

    const grades = computed(() => {
      const grades = regularGradeColors.value.map((color, index) => {
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
    const data = computed(() => {
      return {
        name: gymName.value,
        grade_set: grades.value,
      };
    });
    const {t} = useI18n();
    const gymTemplateLink = 'https://viewer.diagrams.net/?tags=%7B%7D&' +
        'highlight=0000ff&edit=_blank&layers=1&nav=1&title=generic_gym.png#U' +
        'https%3A%2F%2Fraw.githubusercontent.com%2FHumorloos%2' +
        'Fbouldern-app%2Fmaster%2Ffrontend%2Fcypress%2Ffixtures%2F' +
        'generic_gym.png';
    const mapHintLinkElement = `<a
href="${gymTemplateLink}"
target="_blank"
>${t('gymForm.templateLinkText')}</a>`;

    return {
      form,
      validateForm,
      requiredRule,
      requiredImageRule,
      atLeastOneGradeRule,
      // gym properties
      gymName,
      map,
      mapUrl,
      // grade properties
      regularGradeColors,
      extraColor,
      activeExtraColor,
      toggleExtraColor,
      addGradeSelect,
      removeGradeSelect,
      colorOptions: computed(() => store.state.colors),
      grades,
      gradeIds,
      // general properties
      data,
      mapHintLinkElement,
    };
  },
};
</script>

<style scoped>

</style>
