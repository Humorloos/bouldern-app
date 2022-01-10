<template>
  <vue-form
    :form="form"
    :api-path="'/bouldern/color/'"
    @submitted="onSubmitted"
  >
    <label for="id_name">Name: </label>
    <input
      id="id_name"
      v-model="form.name"
      type="text"
    >
    <input
      id="id_color"
      v-model="form.color"
      data-jscolor=""
      class="jscolor-input"
    >
  </vue-form>
</template>

<script>
import VueForm from '@/components/VueForm';
import jscolor from '@eastdesire/jscolor/jscolor';


export default {
  name: 'CreateColor',
  components: {
    VueForm,
  },
  data() {
    return {
      form: {
        name: '',
        color: '#FF7514',
      },
    };
  },
  /**
   * Installs jscolor (required for jscolor widget to work)
   */
  mounted() {
    jscolor.install();
  },
  methods: {
    /**
     * Redirects to index after form submission
     */
    onSubmitted() {
      this.$router.push('/');
    },
  },
};
</script>

<style scoped>

</style>
