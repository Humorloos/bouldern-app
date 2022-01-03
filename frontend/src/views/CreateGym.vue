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

    <difficulty-level-select
      :options="options"
    />
  </vue-form>
</template>

<script>
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
      form: {
        name: '',
      },
      map: undefined,
      apiPath: '/bouldern/rest/add-gym/',
      options: [{
        'label': 'default',
        'style': {'color': '#FF7514'},
      }],
    };
  },
  computed: {
    ...mapState([
      'authToken',
    ]),
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
