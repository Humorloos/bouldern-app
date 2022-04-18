<template>
  <app-view
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
import GymSearch from '../components/GymSearch.vue';
import AppView from '../components/AppView.vue';

export default {
  name: 'HomeView',
  components: {AppView, GymSearch},
};
</script>

<style scoped/>
