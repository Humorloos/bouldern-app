<template>
  <div
    id="modal-content"
    class="modal"
  >
    <slot />
  </div>
  <a
    href="#modal-content"
    rel="modal:open"
  >New Color</a>
</template>

<script>
import 'jquery-modal/jquery.modal.min.css';
require('jquery-modal');
export default {
  name: 'Modal',
};
</script>
