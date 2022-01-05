<template>
  <h1>Log In</h1>
  <form @submit.prevent="submit">
    <p v-if="error.visible">
      {{ $t('wrongCredentialsMsg') }}
    </p>
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
import {mapGetters, mapState} from 'vuex';

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
    ...mapGetters([
      'isAuthenticated',
    ]),
    ...mapState([
      'user',
      'messages',
    ]),
  },
  methods: {
    submit() {
      this.axios.post('/registration/rest/login/', this.form,
      ).then((result) => {
        this.error = '';
        this.$store.commit('setLoginData', result.data);
      }).catch((error) => {
        console.log(error);
        this.error.visible = true;
        Object.keys(this.form).forEach((key) => this.form[key] = '');
      });
    },
  },
};
</script>

<style scoped>

</style>
