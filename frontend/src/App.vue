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
  mounted() {
    if (window.Cypress) {
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
