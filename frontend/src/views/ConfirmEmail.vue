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
     * Sends the email confirmation key to the validation api
     */
    async function confirmEmail() {
      for (const _ of await store.dispatch('showingSpinner')) {
        await store.state.axios.post(
            '/registration/verify-email/', {key: route.params.key});
      }
    }

    return {confirmEmail};
  },
};
</script>

<style scoped>

</style>
