<template>
  <app-view>
    <template #main>
      <v-container>
        <v-form
          ref="form"
          lazy-validation
        >
          <v-row>
            <v-col>
              <v-text-field
                id="id_name"
                v-model="data.name"
                :label="$t('lblName')"
                type="text"
                :rules="[requiredRule($t('lblName'))]"
              />
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <input
                id="id_color"
                v-model="data.color"
                data-jscolor=""
                class="jscolor-input"
              >
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-btn
                id="submit_button"
                @click="submit"
              >
                {{ $t('lblSave') }}
              </v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-container>
    </template>
  </app-view>
</template>

<script>
/** @file view for creating colors */

import jscolor from '@eastdesire/jscolor/jscolor';
import AppView from '../components/AppView.vue';
import {onMounted, ref} from 'vue';
import {useRouter} from 'vue-router';
import {useStore} from 'vuex';
import {requiredRule} from '../helpers/rules.js';


export default {
  name: 'CreateColor',
  components: {
    AppView,
  },
  setup() {
    const data = ref({
      name: '',
      color: '#FF7514',
    });
    const router = useRouter();
    const store = useStore();
    const form = ref(null);

    /**
     * Redirects to index after form submission
     */
    function submit() {
      form.value.validate().then((result) => {
        if (result.valid) {
          store.dispatch('requestWithJwt', {
            apiPath: '/bouldern/color/',
            data: data.value,
          }).then((response) => {
            store.commit('addColor', response.data);
            router.push('/');
          });
        }
      });
    }

    // Installs jscolor (required for jscolor widget to work)
    onMounted(() => jscolor.install());

    return {
      form,
      data,
      submit,
      requiredRule,
    };
  },
};
</script>

<style scoped>

</style>
