<template>
  <h1>Log In</h1>
  <label for="id_email">E-Mail:</label>
  <input
    id="id_email"
    v-model="username"
    type="text"
  >
  <label for="id_password">Password:</label>
  <input
    id="id_password"
    v-model="password"
    type="password"
  >
  <button @click="submit">
    Submit
  </button>

  <div v-if="isAuthenticated">
    <p>
      Hello, {{ user.email }}. You're at the bouldern index.
    </p>
  </div>
  <div v-else>
    <p>You are not logged in</p>
  </div>
</template>
<script>
import {mapGetters, mapState} from 'vuex';

export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
    };
  },
  computed: {
    ...mapGetters([
      'isAuthenticated',
    ]),
    ...mapState([
      'user',
    ]),
  },
  methods: {
    submit() {
      this.axios.post('/registration/rest/login/', this.$data,
      ).then((result) => this.$store.commit('setLoginData', result.data));
    },
  },
};
</script>

<style scoped>

</style>
