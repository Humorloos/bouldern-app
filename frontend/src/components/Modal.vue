<template>
  <div class="my-modal">
    <div id="ex1" class="modal">
      <slot></slot>
    </div>
    <a href="#ex1" rel="modal:open">New Color</a>
  </div>
</template>

<script>
require('jquery-modal');
export default {
  name: "Modal",
}
</script>

<style scoped>

</style>