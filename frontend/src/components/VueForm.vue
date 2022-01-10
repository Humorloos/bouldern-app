<template>
  <form @submit.prevent="submit">
    <slot />
    <button
      id="submit_button"
    >
      {{ submitButtonLabel }}
    </button>
  </form>
</template>

<script>
/** @file component for submitting forms to apis */

import {mapState} from 'vuex';

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
    /**
     * Submits the form to the specified URL via the specified method and emits
     * the submitted event with * the response
     */
    submit() {
      this.axios(this.apiPath, {
        method: this.method,
        data: this.form,
        headers: {
          'authorization': `Bearer ${this.authToken.token}`,
          'content-type': this.contentType,
        },
      }).then((response) => this.$emit('submitted', response));
    },
  },
};
</script>

<style scoped>

</style>
