<template>
  <v-container>
    <v-col>
      <v-btn
        id="id_confirm_email"
        @click="confirmEmail"
      >
        Confirm E-Mail
      </v-btn>
    </v-col>
  </v-container>
</template>

<script>/** @file view for confirming one's email after registration */
import {useRoute} from 'vue-router';
import {useStore} from 'vuex';


export default {
  setup() {
    const route = useRoute();
    const store = useStore();
    /**
     * The email confirmation key to be sent to the validation api
     *
     * @returns {string} the email confirmation key
     */
    function key() {
      return route.params.key;
    }
    /**
     * Sends the email confirmation key to the validation api
     */
    function confirmEmail() {
      store.state.axios.post(
          '/registration/verify-email/', {key: key()});
    }
    return {
      key,
      confirmEmail,
    };
  },
};
</script>

<style scoped>

</style>
