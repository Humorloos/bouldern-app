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
            <v-form
              ref="form"
              lazy-validation
            >
              <v-container>
                <v-row>
                  <v-text-field
                    id="id_email"
                    v-model="data.email"
                    type="text"
                    :label="$t('lblEmail')"
                    :rules="emailRules"
                  />
                </v-row>
                <v-row>
                  <v-text-field
                    id="id_password"
                    v-model="data.password"
                    type="password"
                    :label="$t('lblPassword')"
                    :rules="[requiredRule($t('lblPassword'))]"
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
        <v-row>
          <v-col>
            <v-alert
              v-model="loginError"
              type="error"
            >
              {{ $t('wrongCredentialsMsg') }}
            </v-alert>
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
import {ref} from 'vue';
import {useRouter} from 'vue-router';
import {emailRules, requiredRule} from '../helpers/rules.js';

export default {
  name: 'Login',
  components: {AppView},
  setup() {
    const form = ref(null);

    const data = ref({email: '', password: ''});
    const store = useStore();

    const loginError = ref(false);
    const router = useRouter();

    /**
     * Submits the login form and in case of success, empties email and password
     * and redirects to the home view
     */
    async function login() {
      form.value.validate().then((result) => {
        if (result.valid) {
          store.dispatch('login', data.value).catch((error) => {
            console.log(error);
            loginError.value = true;
          }).then(() => {
            Object.keys(data.value).forEach((key) => data.value[key] = '');
            router.push('/');
          });
        }
      });
    }

    return {
      form,
      data,
      login,
      loginError,
      emailRules,
      requiredRule,
    };
  },
};
</script>

<style scoped>

</style>
