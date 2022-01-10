<template>
  <h1>sup</h1>
  <div>
    <router-link to="/register">
      Register
    </router-link>
  </div>
  <div>
    <router-link to="/login">
      Log In
    </router-link>
  </div>
  <div>
    <a
      href="#"
      @click="logout"
    >Log Out</a>
  </div>
  <div>
    <router-link to="/create-color">
      Create Color
    </router-link>
  </div>
  <div>
    <router-link to="/create-gym">
      Create Gym
    </router-link>
  </div>
  <div>
    <h2>Gym Map:</h2>
    <form @submit.prevent="openGymMap">
      <input
        id="id_gym-name"
        v-model="gymName"
        type="text"
      >
      <button id="submit_button">
        Open
      </button>
    </form>
  </div>
  <div>
    <a
      href="#"
      @click="deleteAccountAndLogout"
    >Delete Account</a>
  </div>
</template>

<script>
/** @file index view with menu */

import {mapActions, mapMutations, mapState} from 'vuex';

export default {
  name: 'Index',
  data() {
    return {
      gymName: '',
    };
  },
  computed: {
    ...mapState(['user']),
  },
  methods: {
    ...mapMutations(['logout']),
    ...mapActions(['deleteAccountAndLogout']),
    /**
     * Redirects to gym map with name entered in text field
     */
    openGymMap() {
      this.$router.push(`/gym-map/${this.gymName}`);
    },
  },
};
</script>

<style scoped>

</style>
