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
            <v-form
              ref="form"
              lazy-validation
            >
              <v-text-field
                id="id_username"
                v-model="data.username"
                :label="$t('lblUsername')"
                type="text"
                :rules="[ requiredRule( $t('lblUsername')) ]"
              />
              <v-text-field
                id="id_email"
                v-model="data.email"
                :label="$t('lblEmail')"
                type="text"
                :rules="emailRules"
              />
              <password-fields v-model="password" />
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
              v-model="confirmationMailSentAlert"
              type="info"
              transition="slide-y-reverse-transition"
            >
              {{ $t('confirmationEmailAlert', {email: data.email}) }}
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
import {
  emailRules,
  requiredRule,
  matchingPasswordsRule,
} from '../helpers/rules.js';
import PasswordFields from '../components/PasswordFields.vue';

export default {
  name: 'Register',
  components: {PasswordFields, AppView},
  setup() {
    const password = ref('');

    const data = ref({
      password2: password.value,
      password1: password.value,
      email: '',
      username: '',
    });

    const store = useStore();
    const axios = store.state.axios;

    const confirmationMailSentAlert = ref(false);

    const form = ref(null);

    /**
     * Posts the registration form to the registration api
     */
    async function submit() {
      const result = await form.value.validate();
      if (result.valid) {
        for (const _ of await store.dispatch('showingSpinner')) {
          await axios.post('/registration/', data.value);
          confirmationMailSentAlert.value = true;
        }
      }
    }

    return {
      form,
      password,
      data,
      submit,
      confirmationMailSentAlert,
      emailRules,
      matchingPasswordsRule,
      requiredRule,
    };
  },
};
</script>

<style scoped>

</style>
