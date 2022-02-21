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
          <gym-form
            ref="gymForm"
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
import GymForm from '../components/GymForm.vue';

export default {
  name: 'CreateGym',
  components: {
    GymForm,
    AppView,
    VueForm,
  },
  setup() {
    const store = useStore();
    const requestWithJwt = (options) =>
      store.dispatch('requestWithJwt', options);

    const gymForm = ref(null);
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
      formData.append('map', gymForm.value.map);
      requestWithJwt({
        apiPath: `${apiPath}${response.data.id}/`,
        method: 'PATCH',
        data: formData,
        contentType: 'multipart/form-data',
      });
      router.push('/');
    }
    const form = computed(
        () => gymForm.value !== null ? gymForm.value.form : {});
    return {
      apiPath,
      onSubmitted,
      gymForm,
      form,
    };
  },
};
</script>

<style>
</style>
