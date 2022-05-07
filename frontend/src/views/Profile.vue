<template>
  <app-view>
    <template #main>
      <v-container>
        <v-row>
          <v-col>
            {{ $t('profile.welcomeMsg', {user: user.username}) }}
          </v-col>
        </v-row>

        <v-row>
          <v-col>
            <v-btn @click="logout">
              Log Out
            </v-btn>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-btn
              color="error"
              size="small"
              @click="deleteAccount"
            >
              Delete Account
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </template>
  </app-view>
</template>

<script>
/** @file User profile view for all user related actions */

import AppView from '../components/AppView.vue';
import {computed} from 'vue';
import {useStore} from 'vuex';
import {useRouter} from 'vue-router';

export default {
  name: 'Profile',
  components: {AppView},
  setup() {
    const store = useStore();
    const router = useRouter();

    /**
     * Logs the user out and redirects to the login view
     */
    function logout() {
      store.commit('logout');
      router.push(`/login`);
    }

    /**
     * Deletes the user's account and redirects to the login view
     */
    function deleteAccount() {
      store.dispatch('deleteAccountAndLogout');
      router.push('/login');
    }

    return {
      user: computed(() => store.state.user),
      logout,
      deleteAccount,
    };
  },
};
</script>

<style scoped>

</style>
