<template>
  <div>
    <router-link to="/">
      Home
    </router-link>
  </div>
  <router-view />
</template>

<script>

export default {
  name: 'App',
};
</script>

<style>
html, body, #app {
  height: 99%;
}
</style>
