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
    submit() {
      this.axios(this.apiPath, {
        method: this.method,
        data: this.form,
        headers: {
          'authorization': `Bearer ${this.authToken.token}`,
          'content-type': this.contentType,
        },
      }).then((response) => this.$emit('submitted', response));
      this.$router.push('/');
    },
  },
};
</script>

<style scoped>

</style>
