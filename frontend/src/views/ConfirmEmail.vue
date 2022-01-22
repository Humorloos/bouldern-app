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

<script>
/** @file view for confirming one's email after registration */

export default {
  name: 'ConfirmEmail',
  computed: {
    /**
     * The email confirmation key to be sent to the validation api
     *
     * @returns {string} the email confirmation key
     */
    key() {
      return this.$route.params.key;
    },
  },
  methods: {
    /**
     * Sends the email confirmation key to the validation api
     */
    confirmEmail() {
      this.axios.post('/registration/verify-email/', {key: this.key});
    },
  },
};
</script>

<style scoped>

</style>
