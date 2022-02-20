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
          <grade-list
            ref="gradeList"
            :color-options="colorOptions"
          />
        </vue-form>
      </v-container>
    </template>
  </app-view>
</template>

<script>
/** @file view for creating gyms */

import VueForm from '../components/VueForm.vue';
import {useStore} from 'vuex';
import AppView from '../components/AppView.vue';
import {computed, ref} from 'vue';
import {useRouter} from 'vue-router';
import GradeList from '../components/GradeList.vue';

export default {
  name: 'CreateGym',
  components: {
    GradeList,
    AppView,
    VueForm,
  },
  setup() {
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

    const gradeList = ref(null);

    /**
     * Gets a form with the gym's name and all grades for submission
     *
     * @returns {object} the gym form
     */
    const form = computed(() => {
      let gradeSet;
      if (gradeList.value !== null) {
        gradeSet = gradeList.value.colors.map((color, index) => {
          return {color: color.id, grade: index + 1};
        });
        if (gradeList.value.activeExtraColor) {
          gradeSet.push({
            color: gradeList.value.extraColor.id, grade: null});
        }
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
    return {
      gymName,
      colorOptions,
      form,
      apiPath,
      onSubmitted,
      onFileChange,
      gradeList,
    };
  },
};
</script>

<style>
</style>
