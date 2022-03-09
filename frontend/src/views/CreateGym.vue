<template>
  <app-view>
    <template #main>
      <v-container>
        <v-row>
          <v-col>
            <h1>Create Gym</h1>
          </v-col>
        </v-row>
        <gym-form
          ref="gymForm"
          @save="submit"
        />
      </v-container>
    </template>
  </app-view>
</template>

<script>
/** @file view for creating gyms */

import {useStore} from 'vuex';
import AppView from '../components/AppView.vue';
import {ref} from 'vue';
import {useRouter} from 'vue-router';
import GymForm from '../components/GymForm.vue';

export default {
  name: 'CreateGym',
  components: {
    GymForm,
    AppView,
  },
  setup() {
    const store = useStore();
    const requestWithJwt = (options) =>
      store.dispatch('requestWithJwt', options);

    const gymForm = ref(null);
    const router = useRouter();
    const apiPath = '/bouldern/gym/';
    /**
     * Submits the gym and the gym map image and redirects to index
     */
    function submit() {
      // submit gym data
      requestWithJwt({
        apiPath: apiPath,
        data: gymForm.value.data,
      }).then((response) =>{
      // submit gym map
        const formData = new FormData();
        formData.append('map', gymForm.value.map[0]);
        requestWithJwt({
          apiPath: `${apiPath}${response.data.id}/`,
          method: 'PATCH',
          data: formData,
          contentType: 'multipart/form-data',
        });
        router.push('/');
      });
    }
    return {
      apiPath,
      submit,
      gymForm,
    };
  },
};
</script>

<style>
</style>
