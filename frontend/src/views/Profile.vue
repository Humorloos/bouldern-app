<template>
  <v-dialog v-model="deleteDialog">
    <v-card>
      <v-card-text>
        {{ $t('profile.deleteWarning') }}
      </v-card-text>
      <v-card-actions>
        <v-btn @click="deleteDialog=false">
          {{ $t('profile.cancel') }}
        </v-btn>
        <v-btn
          id="id_delete-account"
          color="error"
          @click="deleteAccount"
        >
          {{ $t('profile.deleteAccount') }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
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
              @click="openDeleteDialog"
            >
              {{ $t('profile.deleteAccount') }}
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
import {ref} from 'vue';

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

    const deleteDialog = ref(false);

    /**
     * Opens the account deletion dialog
     */
    function openDeleteDialog() {
      deleteDialog.value = true;
    }

    return {
      user: computed(() => store.state.user),
      logout,
      openDeleteDialog,
      deleteDialog,
      deleteAccount,
    };
  },
};
</script>

<style scoped>

</style>
