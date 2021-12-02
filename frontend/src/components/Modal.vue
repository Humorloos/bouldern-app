<template>
  <div class="my-modal">
    {{ modalBody }}
  </div>
</template>

<script>
require('jquery-modal');
export default {
  name: "Modal.vue",
  props: {modalBody: String},
}
</script>

<style scoped>

</style>