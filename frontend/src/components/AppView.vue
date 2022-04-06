<template>
  <v-app-bar height="50">
    <slot name="app-bar-left">
      <v-app-bar-nav-icon
        v-if="display.mobile.value"
        @click.stop="drawer = !drawer"
      />
      <v-app-bar-title
        v-if="display.smAndUp.value"
      >
        <p>
          Boulder Holder
        </p>
      </v-app-bar-title>
    </slot>
    <v-spacer />
    <v-progress-circular
      v-show="loading"
      indeterminate
      :size="20"
      :width="2"
    />
    <slot name="app-bar-right" />
  </v-app-bar>
  <v-navigation-drawer
    v-model="drawer"
  >
    <v-list dense>
      <v-list-item
        v-if="!isAuthenticated"
        to="/login"
      >
        <v-list-item-title>Log In</v-list-item-title>
      </v-list-item>
      <div v-if="isAuthenticated">
        <v-list-item
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
        <slot name="app-drawer" />
        <v-list-subheader v-if="favoriteGyms.length > 0">
          Favorite Gyms
        </v-list-subheader>
        <v-list-item
          v-for="(favoriteGym) in favoriteGyms"
          :key="favoriteGym"
          :to="`/gym-map/${favoriteGym}`"
          class="d-block text-truncate"
        >
          {{ favoriteGym }}
        </v-list-item>
        <gym-search v-if="gymSearch" />
        <v-list-item
          to="/create-gym"
        >
          <v-list-item-title>New Gym</v-list-item-title>
        </v-list-item>
      </div>
    </v-list>
    <template #append>
      <v-container>
        <v-row>
          <v-col>
            <v-btn
              variant="plain"
              to="/privacy"
            >
              {{ $t('appView.privacyPolicy') }}
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </template>
  </v-navigation-drawer>
  <v-main>
    <v-alert
      v-for="(alert, index) in alerts"
      :id="`id_alert-${index}`"
      :key="index"
      rounded="0"
      :type="alert.type"
      closable
      @update:model-value="closeAlert(index)"
    >
      {{ alert.message }}
    </v-alert>
    <v-snackbar
      v-for="(message, index) in notifications"
      :key="index"
      :color="message.type"
      :model-value="true"
      :style="{'margin-bottom':`${60*index}px`}"
      bottom
    >
      {{ message.message }}
      <template
        v-if="message.closable"
        #actions
      >
        <v-btn
          color="primary-darken-1"
          variant="text"
          @click="removeNotification(message)"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>
    <slot name="main" />
  </v-main>
</template>

<script>
/**
 * @file This component is a wrapper for all views and provides an app bar and
 * navigation drawer
 */

import {useDisplay} from 'vuetify';
import {computed, ref, watch} from 'vue';
import {useRoute} from 'vue-router';
import {useStore} from 'vuex';
import GymSearch from './GymSearch.vue';

export default {
  components: {GymSearch},
  props: {
    gymSearch: {
      type: Boolean,
      default: true,
    },
    localAlerts: {
      type: Array,
      default: () => [],
    },
  },
  emits: ['update:localAlerts'],
  setup(props, {emit}) {
    // close the app drawer on mobile when loading app
    const display = useDisplay();
    const drawer = ref(!display.mobile.value);
    // Close the app drawer when navigating to another view
    const route = useRoute();

    /**
     * Closes the app drawer when on mobile
     */
    function collapseDrawer() {
      if (display.mobile.value) drawer.value = false;
    }

    watch(route, collapseDrawer);

    const store = useStore();
    const globalAlerts = computed(() => store.state.globalAlerts);

    const alerts = computed(() =>
      globalAlerts.value.concat(props.localAlerts));

    /**
     * Closes the alert with the provided index by removing it either from the
     * global alerts or from the local alerts
     */
    function closeAlert(index) {
      const alert2close = alerts.value[index];
      if (globalAlerts.value.includes(alert2close)) {
        store.commit('removeAlert', alert2close);
      }
      if (props.localAlerts.includes(alert2close)) {
        const newAlerts = props.localAlerts.slice();
        newAlerts.splice(newAlerts.indexOf(alert), 1);
        emit('update:localAlerts', newAlerts);
      }
    }

    return {
      display,
      drawer,
      isAuthenticated: computed(() => store.getters.isAuthenticated),
      favoriteGyms: computed(() => store.state.favoriteGyms),
      user: computed(() => store.state.user),
      loading: computed(() => store.state.loading),
      notifications: computed(() => store.state.notifications),
      removeNotification: (notification) =>
        store.commit('removeNotification', notification),
      collapseDrawer,
      closeAlert,
      alerts,
    };
  },
};
</script>

<style scoped>

</style>
