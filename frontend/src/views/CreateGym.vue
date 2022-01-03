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

    <difficulty-level-select-rest
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
import VueForm from '@/components/VueForm';
import {mapState} from 'vuex';
import DifficultyLevelSelectRest from '@/components/DifficultyLevelSelectRest';

export default {
  name: 'CreateGym',
  components: {
    VueForm,
    DifficultyLevelSelectRest,
  },
  data() {
    return {
      colors: [{
        color: 'white',
        name: 'default',
        id: 0,
      }],
      gymName: '',
      map: undefined,
      apiPath: '/bouldern/rest/add-gym/',
      colorOptions: [],
    };
  },
  computed: {
    ...mapState([
      'authToken',
    ]),
    form() {
      return {
        name: this.gymName,
        difficultylevel_set: this.colors.map((color, index) => {
          return {color: color.id, level: index + 1};
        }),
      };
    },
  },
  created() {
    this.axios.get('/bouldern/rest/add-color/', {
      headers: {
        'authorization': `Bearer ${this.authToken.token}`,
      },
    }).then((response) => {
      this.colorOptions = response.data;
    });
  },
  mounted() {
    require('vue-select/dist/vue-select.css');
  },
  methods: {
    onFileChange(e) {
      this.map = e.target.files[0];
    },
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
    },
    addDifficultySelect() {
      this.colors.push(this.colors.at(-1));
    },
  },
};
</script>

<style scoped>

</style>
