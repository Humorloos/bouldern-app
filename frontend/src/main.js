/** @file vue app entrypoint */

import {createApp} from 'vue';
import App from './App.vue';
import store from './plugins/store';
import VueAxios from 'vue-axios';
import router from './plugins/router';
import i18n from './i18n';
import vuetify from './plugins/vuetify';

createApp(App)
    .use(store)
    .use(VueAxios, store.state.axios)
    .use(router)
    .use(i18n)
    .use(vuetify)
    .mount('#app');
