import en from './locales/en.yaml';
import {createI18n} from 'vue-i18n/index';

export default createI18n({
  locale: 'en', // set locale
  fallbackLocale: 'en', // set fallback locale
  messages: {
    en,
  },
});
