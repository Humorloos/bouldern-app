<template>
  <h2>Sign up</h2>
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
    @click="submit"
  >
    Sign Up
  </button>
</template>

<script>

export default {
  name: 'App',
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
    submit() {
      this.axios.post('/registration/rest/',
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
