import {createApp} from 'vue';
import App from '@/App.vue';
import store from '@/store/index';
import VueAxios from 'vue-axios';
import http from '@/http-common';
import router from '@/router/index';

createApp(App)
    .use(store)
    .use(VueAxios, http)
    .use(router)
    .mount('#app');
