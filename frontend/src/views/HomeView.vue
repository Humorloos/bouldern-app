<template>
  <gym-map
    v-if="activeGym !== null"
  />
  <app-view
    v-else
    :gym-search="false"
  >
    <template #main>
      <v-list>
        <gym-search />
      </v-list>
    </template>
  </app-view>
</template>
<script>
/** @file the view shown at the index */
import GymMap from './GymMap.vue';
import {useStore} from 'vuex';
import GymSearch from '../components/GymSearch.vue';
import AppView from '../components/AppView.vue';

export default {
  name: 'HomeView',
  components: {AppView, GymSearch, GymMap},
  setup() {
    const store = useStore();
    return {
      activeGym: store.state.activeGym,
    };
  },
};
</script>

<style scoped/>
