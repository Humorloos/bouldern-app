<template>
  <app-view v-model:local-alerts="alerts">
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
                v-model="username"
                :label="$t('lblUsername')"
                type="text"
                :rules="[ requiredRule( $t('lblUsername')) ]"
              />
              <v-text-field
                id="id_email"
                v-model="email"
                :label="$t('lblEmail')"
                type="text"
                :rules="emailRules"
              />
              <password-fields
                v-model="password"
                :error-messages="passwordErrorMessages"
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
import {useI18n} from 'vue-i18n';

export default {
  name: 'Register',
  components: {PasswordFields, AppView},
  setup() {
    const password = ref('');
    const email = ref('');
    const username = ref('');

    const store = useStore();
    const axios = store.state.axios;

    const passwordErrorMessages = ref([]);

    const form = ref(null);
    const alerts = ref([]);
    const {t} = useI18n();

    /**
     * Adds the provided alert to the list of alerts if it is not in there yet.
     */
    function showAlert(alert) {
      if (alerts.value.indexOf(alert) === -1) alerts.value.push(alert);
    }

    /**
     * Posts the registration form to the registration api
     */
    async function submit() {
      passwordErrorMessages.value = [];
      const result = await form.value.validate();
      if (result.valid) {
        for (const _ of await store.dispatch('showingSpinner')) {
          try {
            await axios.post('/registration/', {
              email: email.value,
              username: username.value,
              password2: password.value,
              password1: password.value,
            });
            showAlert({
              type: 'success',
              message: t('msgConfirmationEmailSent', {email: email.value}),
            });
          } catch (error) {
            if (error.response.data.non_field_errors) {
              showAlert({
                type: 'error',
                message: error.response.data.non_field_errors.join('\n'),
              });
            }
            if (error.response.data.password1) {
              passwordErrorMessages.value = error.response.data.password1;
            }
          }
        }
      }
    }

    return {
      form,
      password,
      email,
      username,
      submit,
      alerts,
      passwordErrorMessages,
      emailRules,
      matchingPasswordsRule,
      requiredRule,
    };
  },
};
</script>

<style scoped>

</style>
