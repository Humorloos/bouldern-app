<template>
  <v-list-item v-if="isAuthenticated">
    <v-autocomplete
      id="id_find-gym"
      v-model="gymName"
      label="Find Gym"
      :items="gymNames"
      hide-details
      auto-select-first
      flat
      @update:model-value="openGymMap"
    />
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
      gymNames: computed(() => store.state.gymNames),
      gymName,
      openGymMap,
    };
  },
};
</script>

<style scoped>

</style>
