<template>
  <div id="modal-content" class="modal">
    <slot></slot>
  </div>
  <a href="#modal-content" rel="modal:open">New Color</a>
</template>

<script>
require('jquery-modal');
export default {
  name: "Modal",
}
</script>
