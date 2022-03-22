<template>
  <app-view>
    <template #main>
      <v-container>
        <v-col>
          <v-btn
            id="id_confirm_email"
            @click="confirmEmail"
          >
            Confirm E-Mail
          </v-btn>
        </v-col>
      </v-container>
    </template>
  </app-view>
</template>

<script>/** @file view for confirming one's email after registration */
import {useRoute, useRouter} from 'vue-router';
import {useStore} from 'vuex';
import AppView from '../components/AppView.vue';
import {useI18n} from 'vue-i18n';


export default {
  components: {AppView},
  setup() {
    const route = useRoute();
    const router = useRouter();
    const store = useStore();

    const {t} = useI18n();

    /**
     * Sends the email confirmation key to the validation api
     */
    async function confirmEmail() {
      for (const _ of await store.dispatch('showingSpinner')) {
        await store.state.axios.post(
            '/registration/verify-email/', {key: route.params.key});
      }
      store.commit('showAlert', {
        type: 'success',
        message: t('msgEmailConfirmed'),
        closable: true,
      });
      await router.push('/login');
    }

    return {confirmEmail};
  },
};
</script>

<style scoped>

</style>
