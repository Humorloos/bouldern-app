<template>
  <app-view>
    <template #main>
      <v-container>
        <v-row>
          <v-col class="text-h4">
            Log In
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-form>
              <v-container>
                <v-row>
                  <v-col>{{ loginError }}</v-col>
                </v-row>
                <v-row>
                  <v-text-field
                    id="id_username"
                    v-model="form.username"
                    type="text"
                    label="E-Mail"
                  />
                </v-row>
                <v-row>
                  <v-text-field
                    id="id_password"
                    v-model="form.password"
                    type="password"
                    label="Password"
                  />
                </v-row>
                <v-row>
                  <v-col>
                    <v-btn
                      id="submit_button"
                      type="submit"
                      @click="submit"
                    >
                      Log In
                    </v-btn>
                  </v-col>
                  <v-col>
                    <router-link to="/reset-password">
                      Forgot Password?
                    </router-link>
                  </v-col>
                </v-row>
              </v-container>
            </v-form>
          </v-col>
        </v-row>
        <v-row>
          <v-col
            cols="7"
          >
            <p v-if="isAuthenticated">
              {{ $t('welcomeMsg', {user: user.email}) }}
            </p>
            <p v-else>
              {{ $t('notLoggedInMsg') }}
            </p>
          </v-col>
          <v-spacer />
          <v-col
            cols="5"
          >
            <v-btn
              v-if="isAuthenticated"
              @click="logout"
            >
              Log Out
            </v-btn>
            <v-btn
              v-else
              to="/register"
            >
              Register
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </template>
  </app-view>
</template>
<script>
/** @file login view */

import {useStore} from 'vuex';
import AppView from '../components/AppView.vue';
import {computed, ref} from 'vue';

export default {
  name: 'Login',
  components: {AppView},
  setup() {
    const form = ref({username: '', password: ''});
    const store = useStore();

    const login = (form) => store.dispatch('login', form);
    /**
     * Submits the login form to the login api and commits the returned data to
     * the store. In case of error shows an error message.
     */
    function submit() {
      login(form.value).then(
          () => Object.keys(form.value).forEach((key) => form.value[key] = ''));
    }

    return {
      form,
      isAuthenticated: computed(() => store.getters.isAuthenticated),
      user: computed(() => store.state.user),
      loginError: computed(() => store.state.loginError),
      logout: () => store.commit('logout'),
      submit,
    };
  },
};
</script>

<style scoped>

</style>
