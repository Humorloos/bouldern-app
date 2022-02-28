<template>
  <app-view>
    <template #main>
      <v-container>
        <v-row>
          <v-col>
            <h2>Register</h2>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-form>
              <v-text-field
                v-for="(value, name) in form"
                :id="`id_${name}`"
                :key="name"
                v-model="value.value"
                :label="value.label"
                :type="value.type"
              />
              <v-btn
                id="submit_button"
                type="submit"
                @click="submit"
              >
                Register
              </v-btn>
            </v-form>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-alert
              v-model="alert"
              type="info"
              transition="slide-y-reverse-transition"
            >
              {{ $t('confirmationEmailAlert', {email: form.email.value}) }}
            </v-alert>
          </v-col>
        </v-row>
      </v-container>
    </template>
  </app-view>
</template>

<script>
/** @file view for registering */

import AppView from '../components/AppView.vue';
import {ref} from 'vue';
import {useStore} from 'vuex';

export default {
  name: 'Register',
  components: {AppView},
  setup() {
    const form = ref({
      username: {
        type: 'text',
        label: 'Username',
        value: '',
      },
      email: {
        type: 'text',
        label: 'Email',
        value: '',
      },
      password1: {
        type: 'password',
        label: 'Password',
        value: '',
      },
      password2: {
        type: 'password',
        label: 'Confirm password',
        value: '',
      },
    });
    const store = useStore();
    const axios = store.state.axios;

    const alert = ref(false);
    /**
     * Posts the registration form to the registration api
     */
    function submit() {
      axios.post('/registration/',
          Object.keys(form.value).reduce((payload, key) => {
            payload[key] = form.value[key].value;
            return payload;
          }, {})).then(() => {
        alert.value = true;
      });
    }


    return {form, submit, alert};
  },
};
</script>

<style scoped>

</style>
