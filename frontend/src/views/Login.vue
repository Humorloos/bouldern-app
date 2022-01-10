<template>
  <h1>Log In</h1>
  <form @submit.prevent="submit">
    <p>{{ loginError }}</p>
    <label for="id_username">E-Mail:</label>
    <input
      id="id_username"
      v-model="form.username"
      type="text"
    >
    <label for="id_password">Password:</label>
    <input
      id="id_password"
      v-model="form.password"
      type="password"
    >
    <button
      id="submit_button"
      type="submit"
    >
      Log In
    </button>
  </form>

  <div v-if="isAuthenticated">
    <p>
      {{ $t('welcomeMsg', {user: user.email}) }}
    </p>
  </div>
  <div v-else>
    <p>{{ $t('notLoggedInMsg') }}</p>
  </div>
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
