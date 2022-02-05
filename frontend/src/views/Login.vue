<template>
  <app-view>
    <template #main>
      <v-container>
        <v-row>
          <v-col><h1>Log In</h1></v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-form>
              <p>{{ loginError }}</p>
              <v-text-field
                id="id_username"
                v-model="form.username"
                type="text"
                label="E-Mail"
              />
              <v-text-field
                id="id_password"
                v-model="form.password"
                type="password"
                label="Password"
              />
              <v-btn
                id="submit_button"
                type="submit"
                @click="submit"
              >
                Log In
              </v-btn>
            </v-form>
          </v-col>
        </v-row>
        <v-row>
          <v-col
            cols="8"
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
            cols="4"
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

import {mapActions, mapGetters, mapMutations, mapState} from 'vuex';
import AppView from '../components/AppView.vue';

export default {
  name: 'Login',
  components: {AppView},
  data() {
    return {
      form: {
        username: '',
        password: '',
      },
      error: {
        visible: false,
      },
    };
  },
  computed: {
    ...mapGetters({
      isAuthenticated: 'isAuthenticated',
    }),
    ...mapState({
      user: 'user',
      loginError: 'loginError',
    }),
  },
  methods: {
    ...mapActions({
      login: 'login',
    }),
    ...mapMutations({
      logout: 'logout',
    }),
    /**
     * Submits the login form to the login api and commits the returned data to
     * the store. In case of error shows an error message.
     */
    submit() {
      this.login(this.form).then(
          () => Object.keys(this.form).forEach((key) => this.form[key] = ''));
    },
  },
};
</script>

<style scoped>

</style>
