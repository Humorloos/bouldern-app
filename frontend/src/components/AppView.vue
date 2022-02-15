<template>
  <v-app-bar height="50">
    <slot name="app-bar-left">
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
    </slot>
    <v-spacer />
    <slot name="app-bar-right" />
  </v-app-bar>
  <v-navigation-drawer
    v-model="drawer"
  >
    <v-list dense>
      <v-list-item
        v-if="isAuthenticated"
        to="/profile"
      >
        <v-container class="pa-0">
          <v-row>
            <v-col cols="3">
              <v-avatar color="primary">
                {{ user.username[0].toUpperCase() }}
              </v-avatar>
            </v-col>
            <v-col class="align-self-center">
              {{ user.username }}
            </v-col>
          </v-row>
        </v-container>
      </v-list-item>
      <v-list-item
        v-if="!isAuthenticated"
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
      <v-divider v-if="favoriteGyms.length > 0" />
      <v-list-item
        v-for="(favoriteGym) in favoriteGyms"
        :key="favoriteGym"
        :to="`/gym-map/${favoriteGym}`"
        class="d-block text-truncate"
      >
        {{ favoriteGym }}
      </v-list-item>
      <v-divider />
      <v-list-item
        v-if="isAuthenticated"
        to="/create-gym"
      >
        <v-list-item-title>Create Gym</v-list-item-title>
      </v-list-item>
      <gym-search v-if="gymSearch" />
    </v-list>
  </v-navigation-drawer>
  <!--  todo: hide burger menu on desktop-->
  <v-main>
    <slot name="main" />
  </v-main>
</template>

<script>
/**
 * @file todo
 */

import {useDisplay} from 'vuetify';
import {computed, ref, watch} from 'vue';
import {useRoute, useRouter} from 'vue-router';
import {useStore} from 'vuex';
import GymSearch from './GymSearch.vue';

export default {
  components: {GymSearch},
  props: {
    gymSearch: {
      type: Boolean,
      default: true,
    },
  },
  setup() {
    // close the app drawer on mobile when loading app
    const display = useDisplay();
    const drawer = ref(!display.mobile.value);
    // Close the app drawer when navigating to another view
    const route = useRoute();
    watch(route, () => {
      if (display.mobile.value) drawer.value = false;
    });

    const store = useStore();

    return {
      display,
      drawer,
      isAuthenticated: computed(() => store.getters.isAuthenticated),
      favoriteGyms: computed(() => store.state.favoriteGyms),
      user: computed(() => store.state.user),
    };
  },
};
</script>

<style scoped>

</style>
