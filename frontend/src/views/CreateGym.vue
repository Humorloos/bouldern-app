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
            <v-col>
              <color-select
                :id="`id_color-grade-${index + 1}`"
                v-model="colors[index]"
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
    const colors = ref([{
      color: 'white',
      name: '',
      id: 0,
    }]);
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
      return {
        name: gymName.value,
        grade_set: colors.value.map((color, index) => {
          return {color: color.id, grade: index + 1};
        }),
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
     * Adds the last added color again to colors to create new grade
     * select
     */
    function addGradeSelect() {
      colors.value.push(colors.value.at(-1));
    }
    return {
      colors,
      gymName,
      colorOptions,
      form,
      apiPath,
      onSubmitted,
      addGradeSelect,
      onFileChange,
    };
  },
};
</script>

<style>
</style>
