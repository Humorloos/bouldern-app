<template>
  <app-view>
    <template #main>
      <v-container>
        <v-row>
          <v-col><h1>Create Gym</h1></v-col>
        </v-row>
        <vue-form
          :form="form"
          :api-path="apiPath"
          @submitted="onSubmitted"
        >
          <v-row>
            <v-col>
              <v-text-field
                id="id_name"
                v-model="gymName"
                label="Name"
                type="text"
              />
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-file-input
                id="id_map"
                accept="image/*"
                label="Map"
                @change="onFileChange"
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
        </vue-form>
      </v-container>
    </template>
  </app-view>
</template>

<script>
/** @file view for creating gyms */

import VueForm from '../components/VueForm.vue';
import {useStore} from 'vuex';
import ColorSelect from '../components/ColorSelect.vue';
import AppView from '../components/AppView.vue';
import {computed, ref} from 'vue';
import {useRouter} from 'vue-router';

export default {
  name: 'CreateGym',
  components: {
    AppView,
    VueForm,
    ColorSelect,
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

    const gymName = ref('');
    const map = ref(undefined);
    const colorOptions = ref([]);

    const store = useStore();
    const requestWithJwt = (options) =>
      store.dispatch('requestWithJwt', options);

    // Get all possible colors from the api and saves them
    requestWithJwt({
      apiPath: '/bouldern/color/',
      method: 'GET',
    }).then((response) => {
      colorOptions.value = response.data;
    });


    /**
     * Gets a form with the gym's name and all grades for submission
     *
     * @returns {object} the gym form
     */
    const form = computed(() => {
      const gradeSet = colors.value.map((color, index) => {
        return {color: color.id, grade: index + 1};
      });
      if (activeExtraColor.value) {
        gradeSet.push({
          color: extraColor.value.id, grade: null});
      }
      return {
        name: gymName.value,
        grade_set: gradeSet,
      };
    });
    /**
     * Handler for file upload
     *
     * @param event the file upload event
     */
    function onFileChange(event) {
      map.value = event.target.files[0];
    }
    const router = useRouter();
    const apiPath = '/bouldern/gym/';
    /**
     * Submits the gym map image after submitting the gym map form and redirects
     * to index
     *
     * @param response the create response returned from the api after creating
     * the gym
     */
    function onSubmitted(response) {
      const formData = new FormData();
      formData.append('map', map.value);
      requestWithJwt({
        apiPath: `${apiPath}${response.data.id}/`,
        method: 'PATCH',
        data: formData,
        contentType: 'multipart/form-data',
      });
      router.push('/');
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
    return {
      colors,
      extraColor: extraColor,
      activeExtraColor: activeExtraColor,
      toggleExtraColor,
      gymName,
      colorOptions,
      form,
      apiPath,
      onSubmitted,
      onFileChange,
      addGradeSelect,
      removeGradeSelect,
    };
  },
};
</script>

<style>
</style>
