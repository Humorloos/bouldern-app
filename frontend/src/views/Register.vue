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
              <v-text-field
                id="id_password1"
                v-model="data.password1"
                :label="$t('lblPassword')"
                type="password"
                :rules="[
                  requiredRule($t('lblPassword')),
                  matchingPasswordsRule(data.password2),
                ]"
              />
              <v-text-field
                id="id_password2"
                v-model="data.password2"
                :label="$t('lblConfirmPassword')"
                type="password"
                :rules="[
                  requiredRule($t('lblConfirmPassword')),
                  matchingPasswordsRule(data.password1),
                ]"
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

export default {
  name: 'Register',
  components: {AppView},
  setup() {
    const data = ref({password2: '', password1: '', email: '', username: ''});


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
