<template>
  <div>
    <router-link to="/">
      Home
    </router-link>
  </div>
  <router-view />
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
      }
      this.$store.subscribe(storeEventHandler);
      this.$store.subscribeAction(storeEventHandler);
      window['$store'] = this.$store;
    }
  },
};
</script>

<style>
@import '../node_modules/@ionic/core/css/core.css';
@import '../node_modules/@ionic/core/css/ionic.bundle.css';

html, body, #app {
  height: 99%;
}
</style>
