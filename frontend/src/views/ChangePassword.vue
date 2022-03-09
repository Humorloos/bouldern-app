<template>
  <app-view>
    <template #main>
      <v-container>
        <v-form
          ref="form"
          lazy-validation
        >
          <v-row>
            <v-col>Change password</v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-text-field
                id="id_password1"
                v-model="password1"
                :label="$t('lblPassword')"
                type="password"
                :rules="[
                  requiredRule($t('lblPassword')),
                  matchingPasswordsRule(password2)
                ]"
              />
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-text-field
                id="id_password2"
                v-model="password2"
                :label="$t('lblConfirmPassword')"
                type="password"
                :rules="[
                  requiredRule($t('lblConfirmPassword')),
                  matchingPasswordsRule(password1)
                ]"
              />
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-btn
                id="id_submit"
                @click="changePassword"
              >
                Change password
              </v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-container>
    </template>
  </app-view>
</template>

<script>
/** @file view for changing one's password after resetting it */

import AppView from '../components/AppView.vue';
import {ref} from 'vue';
import {useStore} from 'vuex';
import {useRoute} from 'vue-router';
import {matchingPasswordsRule, requiredRule} from '../helpers/rules.js';

export default {
  name: 'ChangePassword',
  components: {AppView},
  setup() {
    const form = ref(null);

    const password1 = ref('');
    const password2 = ref('');

    const store = useStore();
    const axios = store.state.axios;
    const route = useRoute();

    /**
     * Sends a change password request with the entered password to the backend
     */
    function changePassword() {
      form.value.validate().then((result) => {
        if (result.valid) {
          axios.post('/registration/password/reset/confirm/',
              {
                uid: route.params.uid,
                token: route.params.token,
                new_password1: password1.value,
                new_password2: password2.value,
              });
        }
      });
    }

    return {
      form,
      password1,
      password2,
      changePassword,
      matchingPasswordsRule,
      requiredRule,
    };
  },
};
</script>

<style scoped>

</style>
