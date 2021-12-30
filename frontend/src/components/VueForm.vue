<template>
  <form @submit.prevent="submit">
    <slot />
    <button
      id="submit_button"
      @click="submit"
    >
      {{ submitButtonLabel }}
    </button>
  </form>
</template>

<script>
export default {
  name: 'VueForm',
  props: {
    form: {
      type: Object,
      default: () => {},
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
  methods: {
    submit() {
      this.axios.post(this.apiPath, this.form);
    },
  },
};
</script>

<style scoped>

</style>
