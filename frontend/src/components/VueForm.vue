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
  },
  computed: {
    ...mapState([
      'authToken',
    ]),
  },
  methods: {
    submit() {
      this.axios.post(this.apiPath, this.form, {headers: {
        'authorization': `Bearer ${this.authToken.token}`,
        'content-type': 'application/json',
      }});
      this.$router.push('/');
    },
  },
};
</script>

<style scoped>

</style>
