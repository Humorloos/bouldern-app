<template>
  <v-form>
    <slot />
    <v-btn
      id="submit_button"
      @click="submit"
    >
      {{ submitButtonLabel }}
    </v-btn>
  </v-form>
</template>

<script>
/** @file component for submitting forms to apis */

import {mapActions, mapState} from 'vuex';

export default {
  name: 'VueForm',
  props: {
    form: {
      type: Object,
      default: () => {
      },
    },
    apiPath: {
      type: String,
      default: '/',
    },
    submitButtonLabel: {
      type: String,
      default: 'Submit',
    },
    contentType: {
      type: String,
      default: 'application/json',
    },
    method: {
      type: String,
      default: 'POST',
    },
  },
  emits: ['submitted'],
  computed: {
    ...mapState([
      'authToken',
    ]),
  },
  methods: {
    ...mapActions({
      requestWithJwt: 'requestWithJwt',
    }),
    /**
     * Submits the form to the specified URL via the specified method and emits
     * the submitted event with * the response
     */
    submit() {
      this.requestWithJwt({
        apiPath: this.apiPath,
        method: this.method,
        data: this.form,
        contentType: this.contentType,
      }).then((response) => this.$emit('submitted', response));
    },
  },
};
</script>

<style scoped>

</style>
