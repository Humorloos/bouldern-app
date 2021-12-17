<template>
  <span>this is the gym map for gym {{ gymName }}</span>
</template>

<script>
export default {
  name: 'GymMap',
  props: {
    gymName: {
      type: String,
      default: 'wrong',
    },
  },
};
</script>

<style scoped>

</style>
