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
export const requiredImageRule = (v) => v[0].name !== '' ||
  t('msgRequiredField', {field: t('lblMap')});

export const atLeastOneGradeRule = (v) => v.length > 0 || t('msgNoGrades');

export const longEnoughPasswordRule = (v) => v.length >= 8 ||
  t('msgPasswordTooShort');

export const nonNumericPasswordRule = (v) => isNaN(v) ||
  t('msgNumericPassword');
