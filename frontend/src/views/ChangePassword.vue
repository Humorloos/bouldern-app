<template>
  <app-view>
    <template #main>
      <v-container>
        <v-row>
          <v-col>Change password</v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-form
              ref="form"
              lazy-validation
            >
              <password-fields v-model="password" />

              <v-btn
                id="id_submit"
                @click="changePassword"
              >
                Change password
              </v-btn>
            </v-form>
          </v-col>
        </v-row>
      </v-container>
    </template>
  </app-view>
</template>

<script>
/** @file view for changing one's password after resetting it */

import AppView from '../components/AppView.vue';
import {ref} from 'vue';
import {useStore} from 'vuex';
import {useRoute, useRouter} from 'vue-router';
import {matchingPasswordsRule, requiredRule} from '../helpers/rules.js';
import PasswordFields from '../components/PasswordFields.vue';
import {useI18n} from 'vue-i18n';

export default {
  name: 'ChangePassword',
  components: {PasswordFields, AppView},
  setup() {
    const form = ref(null);

    const password = ref('');

    const store = useStore();
    const axios = store.state.axios;
    const route = useRoute();
    const router = useRouter();
    const {t} = useI18n();

    /**
     * Sends a change password request with the entered password to the backend
     */
    async function changePassword() {
      const result = await form.value.validate();
      if (result.valid) {
        await axios.post('/registration/password/reset/confirm/',
            {
              uid: route.params.uid,
              token: route.params.token,
              new_password1: password.value,
              new_password2: password.value,
            });
        await store.dispatch('showTemporaryNotification', {
          type: 'success',
          message: t('msgPasswordChanged'),
          closable: true,
        });
        await router.push('/login');
      }
    }

    return {
      form,
      password,
      changePassword,
      matchingPasswordsRule,
      requiredRule,
    };
  },
};
</script>

<style scoped>

</style>
