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
        v-model="form.name"
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
      v-model="form.difficultylevel_set"
      :colors="colors"
    />
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
      form: {
        name: '',
        difficultylevel_set:
          {
            color: 'white',
            name: 'default',
          },
      },
      map: undefined,
      apiPath: '/bouldern/rest/add-gym/',
      colors: [],
    };
  },
  computed: {
    ...mapState([
      'authToken',
    ]),
  },
  created() {
    this.axios.get('/bouldern/rest/add-color/', {
      headers: {
        'authorization': `Bearer ${this.authToken.token}`,
      },
    }).then((response) => {
      this.colors = response.data;
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
  },
};
</script>

<style scoped>

</style>
