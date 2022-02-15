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
                      @click="login"
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
            <p>
              {{ $t('notLoggedInMsg') }}
            </p>
          </v-col>
          <v-spacer />
          <v-col
            cols="5"
          >
            <v-btn
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
import {useRouter} from 'vue-router';

export default {
  name: 'Login',
  components: {AppView},
  setup() {
    const form = ref({username: '', password: ''});
    const store = useStore();

    const router = useRouter();

    /**
     * Submits the login form and in case of success, empties email and password
     * and redirects to the home view
     */
    function login() {
      store.dispatch('login', form.value).then(() => {
        Object.keys(form.value).forEach((key) => form.value[key] = '');
        router.push('/');
      });
    }

    return {
      form,
      login,
      loginError: computed(() => store.state.loginError),
    };
  },
};
</script>

<style scoped>

</style>
