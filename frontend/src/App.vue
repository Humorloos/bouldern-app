<template>
  <v-app>
    <v-app-bar height="50">
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
    </v-app-bar>
    <v-navigation-drawer
      v-model="drawer"
    >
      <v-list-item>
        <v-list-item-title class="text-h5">
          sup
        </v-list-item-title>
      </v-list-item>
      <v-list dense>
        <v-list-item to="/register">
          <v-list-item-title>Register</v-list-item-title>
        </v-list-item>
        <v-list-item to="/login">
          <v-list-item-title>Log In</v-list-item-title>
        </v-list-item>
        <v-list-item @click="logout">
          <v-list-item-title>Log Out</v-list-item-title>
        </v-list-item>
        <v-list-item to="/create-color">
          <v-list-item-title>Create Color</v-list-item-title>
        </v-list-item>
        <v-list-item to="/create-gym">
          <v-list-item-title>Create Gym</v-list-item-title>
        </v-list-item>
        <v-list-item>
          <v-list-item-subtitle class="text-h6">
            Gym Map
          </v-list-item-subtitle>
        </v-list-item>
        <v-list-item>
          <v-text-field
            id="id_gym-name"
            v-model="gymName"
            label="Gym Name"
          />
        </v-list-item>
        <v-list-item>
          <v-btn
            id="submit_button"
            @click="openGymMap"
          >
            Open
          </v-btn>
        </v-list-item>
        <v-list-item>
          <v-btn
            color="error"
            size="small"
            @click="deleteAccountAndLogout"
          >
            Delete Account
          </v-btn>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
/** @file highest level component of bouldern app */

import {mapActions, mapMutations} from 'vuex';

export default {
  name: 'App',
  data() {
    return {
      drawer: false,
      gymName: '',
    };
  },
  watch: {
    /**
     * Closes the app drawer when navigating to another view
     */
    $route(to, from) {
      this.drawer = false;
    },
  },
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
  methods: {
    ...mapMutations({commitLogout: 'logout'}),
    ...mapActions({deleteAccountAndLogout: 'deleteAccountAndLogout'}),
    /**
     * Redirects to gym map with name entered in text field
     */
    openGymMap() {
      this.$router.push(`/gym-map/${this.gymName}`);
    },
    /**
     * Logs the user out and redirects to the login view
     */
    logout() {
      this.commitLogout();
      this.$router.push(`/login`);
    },
  },
};
</script>

<style>
</style>
