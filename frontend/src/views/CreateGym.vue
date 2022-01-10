<template>
  <h1>Create Gym</h1>
  <vue-form
    :form="form"
    :api-path="apiPath"
    @submitted="onSubmitted"
  >
    <div>
      <label for="id_name">Name: </label>
      <input
        id="id_name"
        v-model="gymName"
        type="text"
      >
    </div>
    <div>
      <label for="id_map">Map: </label>
      <input
        id="id_map"
        type="file"
        @change="onFileChange"
      >
    </div>

    <difficulty-level-select
      v-for="(color, index) in colors"
      :id="`id_color-level-${index + 1}`"
      :key="color.name"
      v-model="colors[index]"
      :color-options="colorOptions"
    />
    <button
      id="add-level-button"
      type="button"
      @click="addDifficultySelect"
    >
      Add Level
    </button>
  </vue-form>
</template>

<script>
/** @file view for creating gyms */

import VueForm from '@/components/VueForm';
import {mapState} from 'vuex';
import DifficultyLevelSelect from '@/components/DifficultyLevelSelect';

export default {
  name: 'CreateGym',
  components: {
    VueForm,
    DifficultyLevelSelect,
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
     * Gets a form with the gym's name and all difficulty levels for submission
     *
     * @returns {object} the gym form
     */
    form() {
      return {
        name: this.gymName,
        difficultylevel_set: this.colors.map((color, index) => {
          return {color: color.id, level: index + 1};
        }),
      };
    },
  },
  /**
   * Gets all possible colors from the api and saves them
   */
  created() {
    this.axios.get('/bouldern/color/', {
      headers: {
        'authorization': `Bearer ${this.authToken.token}`,
      },
    }).then((response) => {
      this.colorOptions = response.data;
    });
  },
  /**
   * Imports css styles for vue-select component
   */
  mounted() {
    require('vue-select/dist/vue-select.css');
  },
  methods: {
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
      this.axios.patch(`${this.apiPath}${response.data.id}/`, formData,
          {
            headers: {
              'authorization': `Bearer ${this.authToken.token}`,
              'content-type': 'multipart/form-data',
            },
          });
      this.$router.push('/');
    },
    /**
     * Adds the last added color again to colors to create new difficulty level
     * select
     */
    addDifficultySelect() {
      this.colors.push(this.colors.at(-1));
    },
  },
};
</script>

<style>
/*todo: check where we have to import this, here or via require, prefer here*/
@import '../../node_modules/vue-select/dist/vue-select.css';
</style>
