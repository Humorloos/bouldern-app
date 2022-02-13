<template>
  <app-view>
    <template #main>
      <v-container>
        <v-row>
          <v-col>{{ $t('resetPasswordInstructions') }}</v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-text-field
              id="id_email"
              v-model="email"
              label="E-Mail"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-btn
              id="id_send"
              @click="sendPasswordResetEmail"
            >
              Send
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </template>
  </app-view>
</template>

<script>
/** @file todo */
import AppView from '../components/AppView.vue';
import {ref} from 'vue';
import {useStore} from 'vuex';

export default {
  name: 'ResetPassword',
  components: {AppView},
  setup() {
    const email = ref('');

    const store = useStore();
    const axios = store.state.axios;
    /**
     * todo
     */
    function sendPasswordResetEmail() {
      axios.post('/registration/password/reset/', {email: email.value});
    }
    return {email, sendPasswordResetEmail};
  },
};
</script>

<style scoped>

</style>
