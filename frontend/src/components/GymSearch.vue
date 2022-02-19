<template>
  <v-list-subheader>
    Find Gym
  </v-list-subheader>
  <v-list-item v-if="isAuthenticated">
    <v-text-field
      id="id_gym-name"
      v-model="gymName"
      label="Gym Name"
      @keyup.enter="openGymMap"
    />
  </v-list-item>
  <v-list-item v-if="isAuthenticated">
    <v-btn
      id="submit_button"
      @click="openGymMap"
    >
      Open
    </v-btn>
  </v-list-item>
</template>

<script>
/** @file component for searching a gym */
import {computed, ref} from 'vue';
import {useRouter} from 'vue-router';
import {useStore} from 'vuex';

export default {
  name: 'GymSearch',
  setup() {
    const gymName = ref('');

    const router = useRouter();

    /**
     * Redirects to gym map with name entered in text field
     */
    function openGymMap() {
      router.push(`/gym-map/${gymName.value}`);
    }

    const store = useStore();

    return {
      isAuthenticated: computed(() => store.getters.isAuthenticated),
      gymName,
      openGymMap,
    };
  },
};
</script>

<style scoped>

</style>
