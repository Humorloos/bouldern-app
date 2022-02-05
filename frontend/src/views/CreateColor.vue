<template>
  <app-view>
    <template #main>
      <v-container>
        <v-row>
          <v-col>
            <vue-form
              :form="form"
              :api-path="'/bouldern/color/'"
              @submitted="onSubmitted"
            >
              <v-text-field
                id="id_name"
                v-model="form.name"
                label="Name"
                type="text"
              />
              <input
                id="id_color"
                v-model="form.color"
                data-jscolor=""
                class="jscolor-input"
              >
            </vue-form>
          </v-col>
        </v-row>
      </v-container>
    </template>
  </app-view>
</template>

<script>
/** @file view for creating colors */

import VueForm from '../components/VueForm.vue';
import jscolor from '@eastdesire/jscolor/jscolor';
import AppView from '../components/AppView.vue';


export default {
  name: 'CreateColor',
  components: {
    AppView,
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
