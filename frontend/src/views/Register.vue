<template>
  <app-view>
    <v-container>
      <v-row>
        <v-col>
          <h2>Register</h2>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-form>
            <v-text-field
              v-for="(value, name) in form"
              :id="`id_${name}`"
              :key="name"
              v-model="value.value"
              :label="value.label"
              :type="value.type"
            />
            <v-btn
              id="submit_button"
              type="submit"
              @click="submit"
            >
              Register
            </v-btn>
          </v-form>
        </v-col>
      </v-row>
    </v-container>
  </app-view>
</template>

<script>
/** @file view for registering */

import AppView from '../components/AppView.vue';

export default {
  name: 'Register',
  components: {AppView},
  data() {
    return {
      form: {
        username: {
          type: 'text',
          label: 'Username',
          value: '',
        },
        email: {
          type: 'text',
          label: 'Email',
          value: '',
        },
        password1: {
          type: 'password',
          label: 'Password',
          value: '',
        },
        password2: {
          type: 'password',
          label: 'Password confirmation',
          value: '',
        },
      },
    };
  },
  methods: {
    /**
     * Posts the registration form to the registration api
     */
    submit() {
      this.axios.post('/registration/',
          Object.keys(this.form).reduce((payload, key) => {
            payload[key] = this.form[key].value;
            return payload;
          }, {}));
    },
  },
};
</script>

<style scoped>

</style>
