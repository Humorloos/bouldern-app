/** @file todo */
import i18n from '../i18n';


const {t} = i18n.global;
export const requiredRule = (label) => (v) => !!v ||
  t('msgRequiredField', {field: label});

export const matchingPasswordsRule = (password) => (v) => v === password ||
    t('msgPasswordsDoNotMatch');
export const emailRules = [
  requiredRule(t('lblEmail')),
  (v) => new RegExp([
    /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))/,
    /@([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}$/,
  ].map((r) => r.source).join(''),
  ).test(v) || t('msgInvalidEmail'),
];
