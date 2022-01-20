/** @file i18n configuration */

import en from './locales/en.json';
import {createI18n} from 'vue-i18n';

export default createI18n({
  locale: 'en', // set locale
  fallbackLocale: 'en', // set fallback locale
  messages: {
    en,
  },
});
