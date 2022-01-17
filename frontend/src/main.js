/** @file vue app entrypoint */

import {createApp} from 'vue';
import App from '@/App.vue';
import store from '@/store/index';
import VueAxios from 'vue-axios';
import router from '@/router/index';
import i18n from '@/i18n';
import {IonicVue} from '@ionic/vue';

createApp(App)
    .use(store)
    .use(VueAxios, store.state.axios)
    .use(router)
    .use(i18n)
    .use(IonicVue)
    .mount('#app');
