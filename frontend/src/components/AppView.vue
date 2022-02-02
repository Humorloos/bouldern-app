<template>
  <v-app-bar height="50">
    <v-app-bar-nav-icon
      v-if="display.mobile"
      @click.stop="drawer = !drawer"
    />
    <v-app-bar-title
      style="cursor:pointer"
      @click="$router.push('/')"
    >
      Boulder Holder
    </v-app-bar-title>
    <v-spacer />
    <slot name="app-bar-right" />
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
      <v-list-item
        v-if="isAuthenticated"
        @click="logout"
      >
        <v-list-item-title>Log Out</v-list-item-title>
      </v-list-item>
      <v-list-item
        v-else
        to="/login"
      >
        <v-list-item-title>Log In</v-list-item-title>
      </v-list-item>
      <v-list-item
        v-if="isAuthenticated"
        to="/create-color"
      >
        <v-list-item-title>Create Color</v-list-item-title>
      </v-list-item>
      <v-list-item
        v-if="isAuthenticated"
        to="/create-gym"
      >
        <v-list-item-title>Create Gym</v-list-item-title>
      </v-list-item>
      <v-list-item v-if="isAuthenticated">
        <v-list-item-subtitle class="text-h6">
          Gym Map
        </v-list-item-subtitle>
      </v-list-item>
      <v-list-item v-if="isAuthenticated">
        <v-text-field
          id="id_gym-name"
          v-model="gymName"
          label="Gym Name"
          @keyup.enter="openGymMap"
        />
      </v-list-item>
      <v-list-item v-if="isAuthenticated">
        <v-btn
          id="submit_button"
          @click="openGymMap"
        >
          Open
        </v-btn>
      </v-list-item>
      <v-list-item v-if="isAuthenticated">
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
    <slot name="main" />
  </v-main>
</template>

<script>
/**
 * @file
 */

import {useDisplay} from 'vuetify';
import {computed, onMounted, ref, watch} from 'vue';
import {useRoute, useRouter} from 'vue-router';
import {useStore} from 'vuex';

export default {
  setup() {
    // close the app drawer on mobile when loading app
    const display = useDisplay();
    const drawer = ref(!display.mobile.value);
    // Close the app drawer when navigating to another view
    const route = useRoute();
    watch(route, () => {
      if (display.mobile.value) drawer.value = false;
    });

    const gymName = ref('');
    const router = useRouter();
    /**
     * Redirects to gym map with name entered in text field
     */
    function openGymMap() {
      router.push(`/gym-map/${gymName.value}`);
    }

    const store = useStore();
    /**
     * Logs the user out and redirects to the login view
     */
    function logout() {
      store.commit('logout');
      router.push(`/login`);
    }

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
        this.$store.subscribe(storeEventHandler);
        this.$store.subscribeAction(storeEventHandler);
        window['$store'] = this.$store;
      }
    });

    return {
      display,
      drawer,
      gymName,
      openGymMap,
      logout,
      isAuthenticated: computed(() => store.getters.isAuthenticated),
      deleteAccountAndLogout: () => store.dispatch('deleteAccountAndLogout'),
    };
  },
};
</script>

<style scoped>

</style>
