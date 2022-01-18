<template>
  <h2>Register</h2>
  <form @submit.prevent="submit">
    <div
      v-for="(value, name) in form"
      :key="name"
    >
      <label :for="`id_${name}`">{{ value.label }}: </label>
      <input
        :id="`id_${name}`"
        v-model="value.value"
        :type="value.type"
      >
    </div>
    <button
      id="submit_button"
      type="submit"
    >
      Register
    </button>
  </form>
</template>

<script>
/** @file view for registering */

export default {
  name: 'Register',
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
