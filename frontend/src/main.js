import {createApp} from 'vue';
import App from '@/App.vue';
import store from '@/store/index';
import VueAxios from 'vue-axios';
import router from '@/router/index';
import i18n from '@/i18n';

// todo: check for todos in eslint
createApp(App)
    .use(store)
    .use(VueAxios, store.state.axios)
    .use(router)
    .use(i18n)
    .mount('#app');
