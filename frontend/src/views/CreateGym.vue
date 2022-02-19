<template>
  <app-view>
    <template #main>
      <v-container>
        <v-row>
          <v-col><h1>Create Gym</h1></v-col>
        </v-row>
        <v-row>
          <v-col>
            <vue-form
              :form="form"
              :api-path="apiPath"
              @submitted="onSubmitted"
            >
              <v-text-field
                id="id_name"
                v-model="gymName"
                label="Name"
                type="text"
              />
              <v-file-input
                id="id_map"
                accept="image/*"
                label="Map"
                @change="onFileChange"
              />

              <color-select
                v-for="(color, index) in colors"
                :id="`id_color-grade-${index + 1}`"
                :key="color.name"
                v-model="colors[index]"
                :color-options="colorOptions"
              />
              <v-btn
                id="add-grade-button"
                type="button"
                @click="addGradeSelect"
              >
                Add Grade
              </v-btn>
            </vue-form>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-btn
              to="/create-color"
            >
              New Color
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </template>
  </app-view>
</template>

<script>
/** @file view for creating gyms */

import VueForm from '../components/VueForm.vue';
import {mapActions, mapState} from 'vuex';
import ColorSelect from '../components/ColorSelect.vue';
import AppView from '../components/AppView.vue';

export default {
  name: 'CreateGym',
  components: {
    AppView,
    VueForm,
    ColorSelect,
  },
  data() {
    return {
      colors: [{
        color: 'white',
        name: '',
        id: 0,
      }],
      gymName: '',
      map: undefined,
      apiPath: '/bouldern/gym/',
      colorOptions: [],
    };
  },
  computed: {
    ...mapState([
      'authToken',
    ]),
    /**
     * Gets a form with the gym's name and all grades for submission
     *
     * @returns {object} the gym form
     */
    form() {
      return {
        name: this.gymName,
        grade_set: this.colors.map((color, index) => {
          return {color: color.id, grade: index + 1};
        }),
      };
    },
  },
  /**
   * Gets all possible colors from the api and saves them
   */
  created() {
    this.requestWithJwt({
      apiPath: '/bouldern/color/',
      method: 'GET',
    }).then((response) => {
      this.colorOptions = response.data;
    });
  },
  methods: {
    ...mapActions({
      requestWithJwt: 'requestWithJwt',
    }),
    /**
     * Handler for file upload
     *
     * @param event the file upload event
     */
    onFileChange(event) {
      this.map = event.target.files[0];
    },
    /**
     * Submits the gym map image after submitting the gym map form and redirects
     * to index
     *
     * @param response the create response returned from the api after creating
     * the gym
     */
    onSubmitted(response) {
      const formData = new FormData();
      formData.append('map', this.map);
      this.requestWithJwt({
        apiPath: `${this.apiPath}${response.data.id}/`,
        method: 'PATCH',
        data: formData,
        contentType: 'multipart/form-data',
      });
      this.$router.push('/');
    },
    /**
     * Adds the last added color again to colors to create new grade
     * select
     */
    addGradeSelect() {
      this.colors.push(this.colors.at(-1));
    },
  },
};
</script>

<style>
</style>
