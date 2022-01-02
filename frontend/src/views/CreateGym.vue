<template>
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
      <input
        id="id_map"
        type="file"
        @change="onFileChange"
      >
    </div>
  </vue-form>
</template>

<script>
import VueForm from '@/components/VueForm';
import {mapState} from 'vuex';

export default {
  name: 'CreateGym',
  components: {
    VueForm,
  },
  data() {
    return {
      form: {
        name: '',
      },
      map: undefined,
      apiPath: '/bouldern/rest/add-gym/',
    };
  },
  computed: {
    ...mapState([
      'authToken',
    ]),
  },
  methods: {
    onFileChange(e) {
      this.map = e.target.files[0];
    },
    onSubmitted(response) {
      const formData = new FormData();
      formData.append('map', this.map);
      this.axios.patch(`${this.apiPath}${response.data.id}/`, formData,
          {headers: {
            'authorization': `Bearer ${this.authToken.token}`,
            'content-type': 'multipart/form-data',
          }});
    },
  },
};
</script>

<style scoped>

</style>
