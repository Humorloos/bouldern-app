<template>
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
      <v-col>
        <div v-if="isAuthenticated">
          <p>
            {{ $t('welcomeMsg', {user: user.email}) }}
          </p>
        </div>
        <div v-else>
          <p>{{ $t('notLoggedInMsg') }}</p>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
/** @file login view */

import {mapActions, mapGetters, mapState} from 'vuex';

export default {
  name: 'Login',
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
