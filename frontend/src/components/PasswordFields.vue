<template>
  <v-text-field
    id="id_password1"
    :value="modelValue"
    :label="$t('lblPassword')"
    type="password"
    :rules="[
      requiredRule($t('lblPassword')),
      matchingPasswordsRule(password2),
      longEnoughPasswordRule,
      nonNumericPasswordRule,
    ]"
    :error-messages="errorMessages"
    @update:model-value="$emit('update:modelValue', $event)"
  />
  <v-text-field
    id="id_password2"
    v-model="password2"
    :label="$t('lblConfirmPassword')"
    type="password"
    :rules="[
      requiredRule($t('lblConfirmPassword')),
      matchingPasswordsRule(modelValue),
      longEnoughPasswordRule,
      nonNumericPasswordRule,
    ]"
    :error-messages="errorMessages"
  />
</template>

<script>
/** @file password fields with validation */

import {
  longEnoughPasswordRule,
  matchingPasswordsRule, nonNumericPasswordRule,
  requiredRule,
} from '../helpers/rules.js';
import {ref} from 'vue';

export default {
  name: 'PasswordFields',
  props: {
    modelValue: {
      type: String,
      default: '',
    },
    errorMessages: {
      type: Array,
      default: () => [],
    },
  },
  emits: ['update:modelValue'],
  setup() {
    const password2 = ref('');

    return {
      password2,
      requiredRule,
      matchingPasswordsRule,
      longEnoughPasswordRule,
      nonNumericPasswordRule,
    };
  },
};
</script>

<style scoped>

</style>
