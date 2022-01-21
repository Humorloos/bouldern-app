<template>
  <v-app>
    <v-app-bar>
      <v-btn to="/">
        Home
      </v-btn>
    </v-app-bar>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
/** @file highest level component of bouldern app */

export default {
  name: 'App',
  /**
   * Tries to login the user when loading the app and exposes Vuex store to
   * cypress tests
   */
  mounted() {
    if (window.Cypress) {
      const storeEventHandler = (storeEvent, state) => {
        window.Cypress.cy.$log[
            new Date().toISOString() + ' - ' + storeEvent.type] = {
          payload: storeEvent.payload,
        };
      };
      this.$store.subscribe(storeEventHandler);
      this.$store.subscribeAction(storeEventHandler);
      window['$store'] = this.$store;
    }
  },
};
</script>

<style>
html, body, #app {
  height: 99%;
}
</style>
