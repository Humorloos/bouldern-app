import {createApp} from 'vue';
import App from './App.vue';
import VueAxios from 'vue-axios';
import http from '@/http-common';

createApp(App)
    .use(VueAxios, http)
    .mount('#app');
