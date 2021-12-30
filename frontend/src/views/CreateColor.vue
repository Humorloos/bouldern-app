<template>
  <vue-form
    :form="form"
    :api-path="'/bouldern/rest/add-color/'"
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
  mounted() {
    jscolor.install();
  },
};
</script>

<style scoped>

</style>
