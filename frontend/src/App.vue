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

import {mapActions} from 'vuex';

export default {
  name: 'App',
  /**
   * Tries to login the user when loading the app and exposes Vuex store to
   * cypress tests
   */
  mounted() {
    if (window.Cypress) {
      window['$store'] = this.$store;
    }
    this.loginFromStorage();
  },
  methods: {
    ...mapActions({
      loginFromStorage: 'loginFromStorage',
    }),
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
