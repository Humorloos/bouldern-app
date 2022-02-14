<template>
  <v-app>
    <router-view />
  </v-app>
</template>

<script>
/** @file highest level component of bouldern app */

import {onMounted} from 'vue';
import {useStore} from 'vuex';

export default {
  setup() {
    const store = useStore();

    store.dispatch('loadFavoriteGyms');

    // Expose Vuex store to cypress tests and attach log hooks when running
    // cypress test
    onMounted(() => {
      if (window.Cypress) {
        const storeEventHandler = (storeEvent) => {
          window.Cypress.cy.$log[
              new Date().toISOString() + ' - ' + storeEvent.type] = {
            payload: storeEvent.payload,
          };
        };
        store.subscribe(storeEventHandler);
        store.subscribeAction(storeEventHandler);
        window['$store'] = store;
      }
    });
  },
};
</script>

<style>
</style>
